from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    url(r'^_ad/', admin.site.urls),
    path(
        'test/',
        include('consistently.apps.repos.urls', namespace='repos')),
    path(
        'api/',
        include('consistently.apps.api.urls', namespace='api')),
    path(
        '',
        include('social_django.urls', namespace='social')),
    url(
        r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework'))
]
