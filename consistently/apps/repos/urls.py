from django.urls import path

from . import views

app_name = 'repos'
urlpatterns = [
    path(
        '',
        views.HomeView.as_view(),
        name='home'),
    path(
        '<slug:github_user>/',
        views.UserRepoListView.as_view(),
        name='user-repo-list'),
]
