from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    url(r'^_ad/', admin.site.urls),
    path(
        'test/',
        include('consistently.apps.repos.urls', namespace='repos')),
    path(
        '',
        include('social_django.urls', namespace='social')),
]
