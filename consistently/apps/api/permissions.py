from rest_framework.permissions import BasePermission
from consistently.apps.repos import permissions


class HasRepoAccess(BasePermission):
    """
    Access denied for private repositories

    and if the user doesn't have admin access to the repo
    @todo - should we support push?
    """

    def has_object_permission(self, request, view, obj):

        if obj.__class__.__name__ == 'Repository':
            repo = obj
        else:
            # then it is an integration
            repo = obj.repo

        return (
            permissions.repo_is_public(repo) and
            permissions.user_is_repo_admin(request.user, repo))
