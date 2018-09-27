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

    # logo_url = serializers.SerializerMethodField('get_logo_url')

    class Meta:
        model = Integration
        fields = (
            'repo', 'integration_type', 'is_active')  # , 'logo_url')

    # @todo - get logo
    # def get_logo_url(self, obj):
        # return obj.get...()


# class IntegrationDetailSerializer(serializers.ModelSerializer):
#     """
#         Individual integration serializer that users the serializer
#         type to
#     """

#     # logo_url = serializers.SerializerMethodField('get_logo_url')

#     class Meta:
#         model = Integration
#         fields = (
#             'repo', 'integration_type', 'is_active')  # , 'logo_url')


# class HTMLValidationSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = HTMLValidation
#         fields = (
#             'repo', 'integration_type',
#             'status_passed',
#             'last_check', 'is_active', 'deployment_delay',
#             'url_to_validate', 'error_count', 'warning_count')


# class IntegrationDetailSerializer(IntegrationListSerializer):

#     def __init__(self, *args, **kwargs):

#         import pdb
#         pdb.set_trace()

#         super(IntegrationDetailSerializer, self).__init__(*args, **kwargs)

#         klass = INTEGRATION_TYPES[self.instance.integration_type]

#         fields = [k.name for k in klass._meta.fields]

#         for f in fields:
#             print(f)
#             if f not in self.fields:
#                 self.fields.append(f)
