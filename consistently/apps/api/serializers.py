from rest_framework import serializers
from github import Github
from consistently.apps.repos.models import Repository


class RepositorySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:repository-detail")

    class Meta:
        model = Repository
        fields = (
            'url', 'id', 'github_id', 'full_name', 'last_commit',
            'last_commit_name', 'prefix', 'name', 'added_by')


class RepoCreateSerializer(serializers.ModelSerializer):
    """
    Creates a local repository from a gihub repo given an ID

    @todo - permissions
    """

    class Meta:
        model = Repository
        fields = ('github_id',)

    def save(self):

        github_repo = self.get_github_repo(self.validated_data)

        repo = Repository(
            full_name=github_repo.full_name,
            github_id=github_repo.id,
            added_by=self.context['request'].user,
        )
        repo.prefix, repo.name = github_repo.full_name.split('/')
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
            id = data['github_id']
            g = Github()
            self.github_repo = g.get_repo(id)

        return self.github_repo
