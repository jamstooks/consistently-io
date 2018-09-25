from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.urls import reverse, reverse_lazy

from github import Github

from .models import Repository
from consistently.apps.integrations.models import IntegrationStatus


class PrefixRepoListView(TemplateView):
    """
        Shows the list of currently connected repos
        for a given user (or team, hence "prefix")
    """

    template_name = "repos/repo_list.html"

    def get_context_data(self, **kwargs):
        _context = super(PrefixRepoListView, self).get_context_data(**kwargs)

        prefix = kwargs['prefix']

        repo_list = Repository.objects.filter(is_active=True, prefix=prefix)

        if not repo_list:
            raise Http404

        _context['repo_list'] = repo_list
        _context['prefix'] = prefix

        return _context


class RepositoryDetailView(DetailView):

    template_name = "repos/repo_settings.html"
    model = Repository
    context_object_name = "repo"

    def get_object(self, queryset=None):
        return get_object_or_404(
            Repository,
            is_active=True,
            prefix=self.kwargs['prefix'],
            name=self.kwargs['name'])

    def get_context_data(self, **kwargs):
        """
        Get all the integration statuses for the latest commit
        """
        _context = super(RepositoryDetailView, self).get_context_data(**kwargs)
        repo = _context['repo']

        integrationstatus_list = None
        if repo.latest_commit:
            integrationstatus_list = IntegrationStatus.objects.filter(
                commit=repo.latest_commit)

        _context['integrationstatus_list'] = integrationstatus_list
        return _context


class ProfileView(LoginRequiredMixin, TemplateView):

    template_name = "repos/profile.html"
    login_url = reverse_lazy('social:begin', args=['github', ])

    def get_context_data(self, **kwargs):

        _context = super(ProfileView, self).get_context_data(**kwargs)
        _context['main_js'] = settings.REACT_JS_PATH
        _context['main_css'] = settings.REACT_CSS_PATH
        return _context


# class ProfileView(TemplateView):
#     """
#         Where a user configures his/her connected repositories

#         @todo
#             - permissions: auth required, access to github repos
#     """
#     template_name = "repos/profile2.html"

#     def get_context_data(self, **kwargs):

#         context = super().get_context_data(**kwargs)

#         prefix = kwargs['github_prefix']
#         context['prefix'] = prefix

#         github = self.request.user.social_auth.get(provider='github')
#         token = github.extra_data['access_token']
#         g = Github(token)
#         named_user = g.get_user(prefix)
#         auth_user = g.get_user()
#         github_repo_list = named_user.get_repos()

#         context['github_org_list'] = auth_user.get_orgs()

#         connected_repo_id_list = Repository.objects.filter(
#             prefix=prefix).values_list('github_id', flat=True)

#         repo_list = []
#         for repo in github_repo_list:
#             repo_list.append({
#                 'github_id': repo.id,
#                 'name': repo.name,
#                 'full_name': repo.full_name,
#                 'is_connected': repo.id in connected_repo_id_list,
#                 'settings_url': reverse(
#                     'repos:repo-settings', args=repo.full_name.split('/'))
#             })

#         context['repo_list'] = repo_list
#         context['repo_list_api_url'] = "#"  # reverse('api:repository-list')

#         return context


# class HomeView(TemplateView):

#     template_name = 'home.html'

# def get(self, request, *args, **kwargs):
#     if self.request.user.is_authenticated:
#         url = reverse(
#             'repos:user-repo-list',
#             args=(self.request.user.username, ))
#         return redirect(url)

#     return super(HomeView, self).get(request, *args, **kwargs)


# class RepoSettingsView(DetailView):

#     template_name = "repos/repo_settings.html"
#     model = Repository
#     context_object_name = "repo"

#     def get_object(self, queryset=None):
#         return get_object_or_404(
#             Repository,
#             prefix=self.kwargs['github_prefix'],
#             name=self.kwargs['name'])
