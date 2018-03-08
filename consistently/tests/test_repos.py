from django.contrib.auth.models import AnonymousUser, User
from django.test import Client, TestCase, RequestFactory
from django.urls import reverse
from social_django.models import UserSocialAuth

from consistently.apps.repos.models import Repository
from consistently.apps.repos.views import UserRepoListView


TEST_USERNAME = 'jamstooks'


class RepoListTestCase(TestCase):
    def setUp(self):
        
        self.repo = Repository(
            github_id=1, name='test', username=TEST_USERNAME)
        self.repo.save()
        
        self.user = User.objects.create(
            username=TEST_USERNAME, password='12345',)
        self.user.set_password('secret') 
        self.user.save()
        
        usa = UserSocialAuth(
            user=self.user,
            provider='github',
            uid='',
            extra_data={'access_token': 'a5503b76904f8fa2c51efabc92a1155a437a7ced'})
        usa.save()
        
        self.url = reverse('repos:user-repo-list', args=(TEST_USERNAME, ))
        self.client = Client()

    def test_other_user(self):
        """
            Other or anon users should see just a list
            of public connected repos for the user.
        """
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['unconnected_repos']), 0)
        self.assertEqual(len(response.context['connected_repos']), 1)
    
    def test_current_user(self):
        """
            An authenticated user should see his/her own repo
        """
        
        login = self.client.login(username='jamstooks', password='secret') 
        response = self.client.get(self.url)
        self.assertEqual(
            response.context['unconnected_repos'].__class__.__name__,
            'PaginatedList')
