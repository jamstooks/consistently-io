from django.contrib.auth.models import AnonymousUser, User
from django.test import Client, TestCase, RequestFactory
from django.urls import reverse

from consistently.apps.repos.models import Repository
from consistently.apps.repos.views import UserRepoListView


TEST_USERNAME = 'jamstooks'


class RepoListTestCase(TestCase):
    def setUp(self):
        
        self.repo = Repository(
            github_id=1, name='test', username=TEST_USERNAME)
        
        self.user = User.objects.create(
            username=TEST_USERNAME, password='12345',)
        self.user.set_password('secret') 
        self.user.save()
        # github = self.request.user.social_auth.get(provider='github')
        # token = github.extra_data['access_token']
        
        class MockSocialAuth:
            def get(self, provider):
                return {'extra_data': 'tokenValue'}
                
        self.user.social_auth = MockSocialAuth()
        
        self.url = reverse('repos:user-repo-list', args=(TEST_USERNAME, ))
        self.client = Client()
        
        # @todo artificially add a connected repository

    def test_other_user(self):
        """
            Other or anon users should see just a list
            of public connected repos for the user.
        """
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['unconnected_repos']), 0)
        self.assertEqual(len(response.context['connected_repos']), 0)
    
    def test_current_user(self):
        """
            An authenticated user should see his/her own repo
        """
        # @todo authenticate a user
        
        # login = self.client.login(username='testuser', password='hello') 
        # response = self.client.get(self.url)
        self.factory = RequestFactory()
        request = self.factory.get('/customer/details')
        request.user = self.user
        response = UserRepoListView.as_view()(request, github_user=TEST_USERNAME)
        self.assertNotEqual(len(response.context['unconnected_repos']), 0)
