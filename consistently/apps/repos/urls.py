from django.urls import path

from . import views

app_name = 'repos'

urlpatterns = [
    path(
        'profile/',
        views.ProfileView.as_view(),
        name='profile'),
    path(
        'g/<slug:prefix>/',
        views.PrefixRepoListView.as_view(),
        name='prefix-repo-list'),
    path(
        'g/<prefix>/<name>/',
        views.RepositoryDetailView.as_view(),
        name='repo-detail'),
    path(
        'g/<prefix>/<name>/badge.svg',
        views.RepositoryBadgeView.as_view(),
        name='repo-badge'),
    path(
        'g/<prefix>/<name>/conf/',
        views.RepositorySettingsView.as_view(),
        name='repo-settings')
]
