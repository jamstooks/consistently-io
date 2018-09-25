from rest_framework.permissions import BasePermission
from github import Github


class HasRepoAccess(BasePermission):
    """
    Access denied for private repositories

    and if the user doesn't have admin access to the repo
    @todo - should we support push?
    """

    def has_object_permission(self, request, view, obj):

        github = request.user.social_auth.get(provider='github')
        token = github.extra_data['access_token']
        g = Github(token)

        if obj.__class__.__name__ == 'Repository':
            repo = g.get_repo(obj.github_id)
        else:
            # then it is an integration
            repo = g.get_repo(obj.repo.github_id)

        # if the repo is private return False
        # only public repos for the beta
        if repo.private:
            return False

        # if the user doesn't have access to the repo return false
        if not repo.permissions.admin:  # and not repo.permissions.push:
            return False

        return True
