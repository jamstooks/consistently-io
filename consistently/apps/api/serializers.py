from rest_framework import serializers
from github import Github
from consistently.apps.repos.models import Repository
from consistently.apps.integrations.models import (
    Integration, INTEGRATION_TYPES)
from consistently.apps.integrations.types.html.models import HTMLValidation


class RepositoryUpdateSerializer(serializers.ModelSerializer):
    """
        Serializer for the `is_active` field on a repository

        @todo - validation here or on the view?
    """

    class Meta:
        model = Repository
        fields = ("is_active", )


class IntegrationListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Integration
        fields = '__all__'
        # fields = ('id', 'integration_type', 'is_active')
