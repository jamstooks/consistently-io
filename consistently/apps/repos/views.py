from django.views.generic.base import TemplateView
from github import Github

class HomePageView(TemplateView):

    template_name = "repos/base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        github = self.request.user.social_auth.get(provider='github')
        token = github.extra_data['access_token']
        g = Github(token)
        user = g.get_user()
        repo_list = user.get_repos()
        context['repo_list'] = repo_list
        
        # import pdb; pdb.set_trace()
        return context