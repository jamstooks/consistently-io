from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.urls import reverse
from github import Github

from .models import Repository


class HomeView(TemplateView):

    template_name = 'repos/home.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            url = reverse(
                'repos:user-repo-list',
                args=(self.request.user.username, ))
            return redirect(url)

        return super(HomeView, self).get(request, *args, **kwargs)


class PrefixRepoListView(TemplateView):
    """
        Shows the list of currently connected repos
        for a given user (or team, hence prefix)
    """

    template_name = "repos/repo_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #@todo - confirm github prefix exists?

        context['github_prefix'] = kwargs['github_prefix']

        connected_repos = Repository.objects.filter(
            prefix=kwargs['github_prefix'])
        context['connected_repos'] = connected_repos

        return context


class ProfileView(TemplateView):
    """
        Where a user configures his/her connected repositories

        @todo
            - permissions: auth required, access to github repos
    """
    template_name = "repos/profile.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        prefix = kwargs['github_prefix']
        context['prefix'] = prefix

        github = self.request.user.social_auth.get(provider='github')
        token = github.extra_data['access_token']
        g = Github(token)
        named_user = g.get_user(prefix)
        auth_user = g.get_user()
        github_repo_list = named_user.get_repos()

        context['github_org_list'] = auth_user.get_orgs()

        connected_repo_id_list = Repository.objects.filter(
            prefix=prefix).values_list('github_id', flat=True)

        repo_list = []
        for repo in github_repo_list:
            repo_list.append({
                'github_id': repo.id,
                'name': repo.name,
                'full_name': repo.full_name,
                'is_connected': repo.id in connected_repo_id_list
            })

        context['repo_list'] = repo_list
        context['repo_list_api_url'] = reverse('api:repository-list')

        return context
