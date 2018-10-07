from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.urls import reverse, reverse_lazy

from github import Github

from .models import Repository
from .permissions import user_is_repo_admin, repo_is_public
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

        repos = Repository.objects.filter(is_active=True, prefix=prefix)

        repo_list = []
        for r in repos:
            repo = {
                'full_name': r.full_name,
                'prefix': r.prefix,
                'name': r.name,
                'url': reverse('repos:repo-detail', args=(r.prefix, r.name)),
                'settings_url': reverse('repos:repo-settings', args=(r.prefix, r.name))
            }
            if r.latest_commit:
                repo.update(r.latest_commit.get_counts())
            repo_list.append(repo)

        if not repo_list:
            raise Http404

        _context['repo_list'] = repo_list
        _context['prefix'] = prefix
        _context['prefix_matches_user'] = (
            self.request.user.is_authenticated and
            prefix == self.request.user.username)

        return _context


class RepoDetailMixin(object):

    model = Repository
    context_object_name = "repo"

    def get_object(self, queryset=None):

        repo = get_object_or_404(
            Repository,
            is_active=True,
            prefix=self.kwargs['prefix'],
            name=self.kwargs['name'])

        if not repo_is_public(repo, user=self.request.user):
            raise Http404

        return repo

    def get_context_data(self, **kwargs):
        _context = super(RepoDetailMixin, self).get_context_data(**kwargs)
        _context['prefix'] = _context['repo'].prefix
        return _context


class RepositoryDetailView(RepoDetailMixin, DetailView):

    template_name = "repos/repo_detail.html"

    def get_context_data(self, **kwargs):
        """
        Get all the integration statuses for the latest commit
        """
        _context = super(RepositoryDetailView, self).get_context_data(**kwargs)
        repo = _context['repo']
        _context['prefix'] = repo.prefix
        _context['is_repo_admin'] = (
            self.request.user.is_authenticated and
            user_is_repo_admin(self.request.user, repo))

        status_list = None
        if repo.latest_commit:
            status_list = IntegrationStatus.objects.filter(
                commit=repo.latest_commit)

        _context['status_list'] = status_list
        return _context


class RepositorySettingsView(LoginRequiredMixin, RepoDetailMixin, DetailView):

    template_name = "repos/repo_settings.html"

    def get_object(self, **kwargs):
        """
        Only repository admins have access to the settings
        """
        repo = super(RepositorySettingsView, self).get_object(**kwargs)
        if not user_is_repo_admin(self.request.user, repo):
            raise PermissionDenied
        return repo

    def get_context_data(self, **kwargs):

        _context = super(RepositorySettingsView,
                         self).get_context_data(**kwargs)
        _context['main_js'] = settings.REACT_JS_PATH
        _context['main_css'] = settings.REACT_CSS_PATH
        return _context


class ProfileView(LoginRequiredMixin, TemplateView):

    template_name = "repos/profile.html"
    login_url = reverse_lazy('social:begin', args=['github', ])

    def get_context_data(self, **kwargs):

        _context = super(ProfileView, self).get_context_data(**kwargs)
        _context['main_js'] = settings.REACT_JS_PATH
        _context['main_css'] = settings.REACT_CSS_PATH
        return _context
