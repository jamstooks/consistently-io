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
        # except Http404:
        #     # redirect here
        #     return redirect(url)
        # context = self.get_context_data(object=self.object)
        # return self.render_to_response(context)

    

class UserRepoListView(TemplateView):

    template_name = "repos/base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        git_user = kwargs['github_user']

        connected_repos = Repository.objects.filter(
            owner__username=kwargs['github_user'])
        context['connected_repos'] = connected_repos
        context['unconnected_repos'] = []

        # this bit might get extracted to a parent class...
        user_is_owner = False
        if self.request.user.is_authenticated:
            if self.request.user.username == git_user:
                user_is_owner = True
        context['user_is_owner'] = user_is_owner

        if user_is_owner:
            # @todo - look into caching this and having a refresh button
            github = self.request.user.social_auth.get(provider='github')
            token = github.extra_data['access_token']
            g = Github(token)
            user = g.get_user()
            repo_list = user.get_repos()
            # i was going to remove the connected repos here, but given the
            # `github.PaginatedList.PaginatedList` object it might be
            # easier to remove this in the template @todo - think about.
            context['unconnected_repos'] = repo_list

        return context
