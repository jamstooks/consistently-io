"""
Permission functions and view decorators

These connect frequently with github and it might make sense
to cache them for short periods to reduce the connections.

@todo - consider caching
"""

from github import Github
from github.GithubException import RateLimitExceededException
import os

GITHUB_APP_TOKEN = os.environ.get('GITHUB_APP_TOKEN')


def user_is_repo_admin(user, repo):
    """
    Evaluates if a user has admin access to a repository
    on github
    """

    # get the users' github connection
    github = user.social_auth.get(provider='github')
    g = Github(github.extra_data['access_token'])

    # get the github repository
    github_repo = g.get_repo(repo.github_id)

    return github_repo.permissions.admin


def repo_is_public(repo, user=None):
    """
    Evaluates if a repo is public on github

    @todo - might have to rate-limit here for non-authenticated users
    """
    if user and user.is_authenticated:
        github = user.social_auth.get(provider='github')
        g = Github(github.extra_data['access_token'])
    else:
        g = Github(GITHUB_APP_TOKEN)

    try:
        gr = g.get_repo(repo.github_id)
        return not gr.private
    except GithubException as e:
        return False
