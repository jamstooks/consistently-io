from rest_framework import serializers
from .models import Coveralls


class CoverallsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coveralls
        fields = ('is_active', 'build_time')
