from rest_framework import serializers
from .models import PageSpeed
from ..validators import RequiredIfActive


class PageSpeedSerializer(serializers.ModelSerializer):

    class Meta:
        model = PageSpeed
        fields = (
            'is_active',
            'url',
            'deployment_delay',
            'use_mobile_strategy')
        validators = [RequiredIfActive(fields=['url'])]
