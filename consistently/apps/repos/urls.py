from django.urls import path

from . import views

app_name = 'repos'

urlpatterns = [
    path(
        'profile/',
        views.ProfileView.as_view(),
        name='profile'),
    path(
        '<slug:prefix>/',
        views.PrefixRepoListView.as_view(),
        name='prefix-repo-list'),
    path(
        '<slug:prefix>/<slug:name>/',
        views.RepositoryDetailView.as_view(),
        name='repo-detail')
]
