from django.shortcuts import get_object_or_404
from django.urls import reverse

from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from github import Github

from consistently.apps.repos.models import Repository
from consistently.apps.integrations.models import Integration, INTEGRATION_TYPES
from consistently.apps.integrations.types.html.models import HTMLValidation
from .serializers import (
    RepositoryUpdateSerializer, IntegrationListSerializer)
from .permissions import HasRepoAccess

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


class IntegrationListView(
        mixins.ListModelMixin, viewsets.GenericViewSet):
    """
        integrations can only be listed by repository

        specific integration types have their own views
    """
    queryset = Integration.objects.all()
    serializer_class = IntegrationListSerializer
    # permission_classes = (IsAuthenticated, HasRepoAccess)

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
