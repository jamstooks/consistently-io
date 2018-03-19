from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import views


app_name = 'api'

router = DefaultRouter()
router.register(r'repos', views.RepositoryViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]
