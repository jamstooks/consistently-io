from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core import serializers
from django.urls import reverse
from django.db.utils import IntegrityError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from github import Github
from json import loads

from consistently.apps.repos.models import Repository, Commit
from consistently.apps.integrations.models import (
    Integration, IntegrationStatus, INTEGRATION_TYPES)
from consistently.apps.integrations.tasks import run_integration

from .serializers import (
    RepositoryUpdateSerializer, IntegrationListSerializer)
from .permissions import HasRepoAccess

import os

# @todo - throttling


class GithubReposView(APIView):
    """
    Lists the available github repos for a logged in user
    along with activation status
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        github = self.request.user.social_auth.get(provider='github')
        token = github.extra_data['access_token']
        g = Github(token)
        user = g.get_user()

        repo_list = []
        # for every github repo
        for gr in user.get_repos():
            if gr.permissions.admin:
                try:
                    repo = Repository.objects.get(github_id=gr.id)
                except Repository.DoesNotExist:
                    # @todo - review performance here,
                    # should these be created here or on activation?
                    # Rationale: to get around having to create an
                    # update_or_create endpoint
                    # @todo - build a cleanup script
                    if not gr.private:
                        repo = Repository.objects.create(
                            github_id=gr.id,
                            prefix=gr.owner.login,
                            name=gr.name
                        )
                if not gr.private:
                    repo_list.append({
                        'id': repo.id,
                        'url': reverse(
                            'repos:repo-detail',
                            kwargs={'prefix': repo.prefix, 'name': repo.name}),
                        'prefix': repo.prefix,
                        'name': repo.name,
                        'github_id': gr.id,
                        'is_active': repo.is_active,
                        'settings_url': reverse(
                            'repos:repo-settings',
                            kwargs={'prefix': repo.prefix, 'name': repo.name}),
                    })

        return Response(repo_list)


class ToggleRepositoryViewSet(generics.UpdateAPIView):
    """
        allows for toggling of `is_active` property for a repository

        @todo - this should add/remove the webhook from github
    """
    queryset = Repository.objects.all()
    serializer_class = RepositoryUpdateSerializer
    lookup_field = 'github_id'
    permission_classes = (IsAuthenticated, HasRepoAccess)

    def update(self, request, *args, **kwargs):
        """
        Set the webhook

        Considered doing this on the save method of the model, but
        felt like the logic was better here.
        """
        response = super(ToggleRepositoryViewSet, self).update(
            request, args, kwargs)

        repo = self.get_object()
        hook_id = repo.hook_id

        # Set up github connection and get the repo reference
        github = self.request.user.social_auth.get(provider='github')
        token = github.extra_data['access_token']
        g = Github(token)
        github_repo = g.get_repo(repo.github_id)

        # If the status is active create (or confirm) the webhook
        if repo.is_active and not repo.hook_id:
            hook_config = {
                'url': "%s%s" % (
                    settings.PUBLIC_URL, settings.WEBHOOK_URL),
                'content_type': "json"
            }

            hook = github_repo.create_hook(
                name="web",
                config={
                    'url': "%s%s" % (
                        settings.PUBLIC_URL, settings.WEBHOOK_URL),
                    'content_type': "json"
                })
            repo.hook_id = hook.id
            repo.save()

        # if the status is inactive remove the webhook
        elif not repo.is_active and repo.hook_id:
            hook = github_repo.get_hook(repo.hook_id)
            hook.delete()
            repo.hook_id = None
            repo.save()

        return response


class IntegrationListView(
        mixins.ListModelMixin, viewsets.GenericViewSet):
    """
        integrations can only be listed by repository

        specific integration types have their own views
    """
    queryset = Integration.objects.all()
    serializer_class = IntegrationListSerializer
    permission_classes = (IsAuthenticated, HasRepoAccess)

    def get_queryset(self):

        # ensure that all available integrations exist for the repo
        repo = Repository.objects.get(github_id=self.kwargs['github_id'])
        for Klass in INTEGRATION_TYPES.values():
            try:
                i = Klass.objects.get(repo=repo)
            except Klass.DoesNotExist:
                Klass.objects.create(repo=repo)

        return Integration.objects.filter(repo=repo)

    def list(self, request, *args, **kwargs):
        """
        Each integration should use the right serializer
        """
        queryset = self.get_queryset()
        data = []
        for integration in queryset:
            # serializerClass = integration.type_instance.get_serializer_class()
            instance = integration.type_instance
            serializer = self.serializer_class(instance)
            data.append(serializer.data)
        return Response(data)


class IntegrationDetailView(
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        viewsets.GenericViewSet):
    """
    Retrive/Update endpoint for a specific integration
    """
    queryset = Integration.objects.all()
    serializer_class = IntegrationListSerializer
    permission_classes = (IsAuthenticated, HasRepoAccess)

    def get_object(self):
        i = get_object_or_404(
            Integration,
            repo__github_id=self.kwargs['github_id'],
            pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, i)
        return i.type_instance

    def get_serializer_class(self):
        return self.get_object().get_serializer_class()


@method_decorator(csrf_exempt, name='dispatch')
class GithubWebhookView(APIView):
    """
    handles webooks connectons from github

    @todo - this definitely could be more robust.
    """

    def post(self, request, format=None):

        try:
            obj = loads(request.body)
            github_id = obj['repository']['id']

            # Initial hook creation
            if "hook_id" in obj.keys():
                return Response(data={
                    'status': "ACCEPTED",
                    'message': "Thanks for connecting with Consistently.io!"
                }, status=200)

            # See if the repo exists locally
            try:
                repo = Repository.objects.get(github_id=github_id)
            except:
                return Response(data={
                    'status': "REJECTED",
                    'message': "Repository does not exist on Consistently.io"
                }, status=400)

            # Only process active repos
            if not repo.is_active:
                return Response(data={
                    'status': "REJECTED",
                    'repo': repo.name,
                    'message': "Repository not active on Consistently.io"
                }, status=400)

            # Only process public repos
            # @todo - consider deactivating repo
            if obj['repository']['private']:
                return Response(data={
                    'status': "REJECTED",
                    'repo': repo.name,
                    'message': "Repository not public"
                }, status=400)

            # accept only pushes to master
            if obj['ref'] != "refs/heads/master":
                return Response(data={
                    'status': "REJECTED",
                    'repo': repo.name,
                    'message': "Does not apply to master"
                }, status=400)

            commit_id = obj['head_commit']['id']

            # add a new commit to the repository
            try:
                commit = Commit.objects.create(
                    repo=repo,
                    sha=obj['head_commit']['id'],
                    message=obj['head_commit']['message'],
                    github_timestamp=obj['head_commit']['timestamp']
                )
                # @todo - there may be a race condition here
                # we might need to do a timestamp compare
                repo.latest_commit = commit
                repo.save()
            except IntegrityError:
                return Response(data={
                    'status': "REJECTED",
                    'repo': repo.name,
                    'commit': obj['head_commit']['id'],
                    'message': "Commit already received"
                }, status=400)

            # queue up worker to... (process commit)

            #  identify all active integrations for this repository
            active_integrations = []
            for Klass in INTEGRATION_TYPES.values():
                try:
                    i = Klass.objects.get(repo=repo)
                    if i.is_active:
                        active_integrations.append(i)
                except Klass.DoesNotExist:
                    # there may be a few instances where new integrations
                    # haven't been created for the repo yet.
                    pass

            # create `IntegrationStatus` objects for each integration
            for i in active_integrations:

                data = serializers.serialize('json', [i, ])
                status = IntegrationStatus.objects.create(
                    integration=i, commit=commit, with_settings=data)

                #  queue up worker for each IntegrationStatus
                print("triggering task")
                task = run_integration.apply_async(
                    args=(status.id,),
                    kwargs=i.get_task_kwargs(),
                    countdown=i.get_task_delay())

                # store the task id on the status object
                # but only update the task_id in case the
                # task has already modified the status
                status.task_id = task.id
                status.save(update_fields=["task_id"])

            # log the latest commit
            return Response(data={
                'status': "ACCEPTED",
                'repo': repo.name,
                'commit': commit.sha,
                'integrations': [i.integration_type for i in active_integrations]
            }, status=200)

        except Exception as e:
            message = (e.__class__.__name__, str(e))
            print(message)
            return Response(data={
                'status': "ERROR",
                'message': "%s: %s" % message
            }, status=500)
