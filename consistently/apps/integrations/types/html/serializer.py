from rest_framework import serializers
from .models import HTMLValidation
from ..validators import RequiredIfActive


class HTMLValidationSerializer(serializers.ModelSerializer):

    class Meta:
        model = HTMLValidation
        fields = ('is_active', 'url_to_validate', 'deployment_delay')
        validators = [RequiredIfActive(fields=['url_to_validate'])]
