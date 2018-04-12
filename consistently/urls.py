from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from django.urls import include, path


""" @todo
    - find a better place for logout.
    - add prefix to social auth 
"""


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return redirect('/g/')


urlpatterns = [
    url(r'^_ad/', admin.site.urls),
    path(
        'api/',
        include('consistently.apps.api.urls', namespace='api')),
    path(
        'g/',
        include('consistently.apps.repos.urls')),
    path('logout/', logout, name='logout'),
    url(
        r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')),
    url('', include('social_django.urls')), # why can't this have a prefix??
    
]
