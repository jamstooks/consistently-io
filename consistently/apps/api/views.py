from consistently.apps.repos.models import Repository
from .serializers import RepositorySerializer, RepoCreateSerializer

from django.http import Http404
from github import Github
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class RepositoryViewSet(viewsets.ModelViewSet):
    """
        list all repositories
    """
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer

    def get_serializer_class(self):
        if self.request.method == "POST":
            return RepoCreateSerializer
        return self.serializer_class


class GithubReposView(APIView):
    """
    Lists the available github repos for a logged in user
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        github = self.request.user.social_auth.get(provider='github')
        token = github.extra_data['access_token']
        g = Github(token)
        user = g.get_user()

        repo_list = []
        for r in user.get_repos():
            repo_list.append({'full_name': r.full_name, 'id': r.id})

        # @todo - decide on permissions here... what access level
        # to a github repo grants this?

        return Response(repo_list)
