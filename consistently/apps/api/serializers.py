from rest_framework import serializers
from github import Github
from consistently.apps.repos.models import Repository


class RepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository
        fields = (
            'github_id', 'last_commit', 'last_commit_name', 'name', 'owner')


class RepoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository
        fields = ('name', 'owner')
        
    def save(self):

        github_repo = self.get_github_repo(self.validated_data)
        
        repo = Repository(
            name=self.validated_data['name'],
            owner=self.validated_data['owner'],
            github_id=github_repo.id)
        repo.save()
    
    def validate(self, data):
        """
        Check that the github repo exists
        """
        github_repo = self.get_github_repo(data)
        
        try:
            id = github_repo.id
        except:
            raise serializers.ValidationError("No matching repo on Github")
        return data
    
    def get_github_repo(self, data):

        if not hasattr(self, 'github_repo'):
            owner = data['owner']
            name = data['name']
            full_name = "%s/%s" % (owner.username, name)
            g = Github()
            self.github_repo = g.get_repo(full_name)

        return self.github_repo