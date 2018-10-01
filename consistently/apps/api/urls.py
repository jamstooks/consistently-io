from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url, include
from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views


app_name = 'api'

router = DefaultRouter()
# router.register(r'repos', views.ToggleRepositoryViewSet)
# router.register(r'integrations', views.IntegrationViewSet)
# router.register(r'integrations-html', views.HTMLValidationViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),

    # url(
    #     r'^integration-type/<slug:type>/<id:id>/',
    #     views.HTMLValidationViewSet.as_view(),
    #     name='integration-types'),

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
        name='integration-detail')
]
