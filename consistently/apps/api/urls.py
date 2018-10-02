from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url, include
from django.urls import path
from . import views


app_name = 'api'

urlpatterns = [
    path(
        'profile-repos/',
        views.GithubReposView.as_view(),
        name='profile-repos'),
    path(
        'toggle-repo/<int:github_id>/',
        views.ToggleRepositoryViewSet.as_view(),
        name='toggle-repo'),
    path(
        'integrations/<int:github_id>/',
        views.IntegrationListView.as_view({'get': 'list'}),
        name='integration-list'),
    path(
        'integrations/<int:github_id>/<int:pk>/',
        views.IntegrationDetailView.as_view(
            {'get': 'retrieve', 'patch': 'update'}),
        name='integration-detail'),

    path(
        'consistently-io-github-webhook/',
        views.GithubWebhookView.as_view(),
        name="github-webhook"
    )
]
