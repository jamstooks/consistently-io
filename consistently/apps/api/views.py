from consistently.apps.repos.models import Repository
from .serializers import RepositorySerializer, RepoCreateSerializer

from django.http import Http404
from github import Github
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets


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
