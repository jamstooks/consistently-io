from django.urls import path

from . import views

app_name = 'repos'

urlpatterns = [
    path(
        '',
        views.HomeView.as_view(),
        name='home'),
    path(
        'profile/<slug:github_prefix>/',
        views.ProfileView.as_view(),
        name='profile'),
    path(
        '<slug:github_prefix>/',
        views.PrefixRepoListView.as_view(),
        name='user-repo-list'),
]
