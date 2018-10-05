from rest_framework import serializers
from .models import Travis


class TravisSerializer(serializers.ModelSerializer):

    class Meta:
        model = Travis
        fields = ('is_active', 'build_time')
