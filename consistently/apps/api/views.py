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
    @todo - validate owner and that github repo exists
    """
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return RepoCreateSerializer
        return self.serializer_class


# class RepositoryListView(APIView):
#     """
#     List all snippets, or create a new snippet.
#     """
#     def get(self, request, format=None):
#         snippets = Repository.objects.all()
#         serializer = RepositorySerializer(snippets, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         create_serializer = RepoCreateSerializer(data=request.data)
#         if create_serializer.is_valid():
            
#             github = self.request.user.social_auth.get(provider='github')
#             token = github.extra_data['access_token']
#             g = Github(token)
#             user = g.get_user()
#             import pdb; pdb.set_trace()
            
#             serializer = RepositorySerializer(repo)
            
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
