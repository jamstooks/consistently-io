from django.urls import path

from . import views

app_name = 'repos'
urlpatterns = [
    path(
        '<slug:github_user>/',
        views.UserRepoListView.as_view(),
        name='user-repo-list'),
]
