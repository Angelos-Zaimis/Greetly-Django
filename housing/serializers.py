

from housing.models import Housing
from rest_framework import serializers

class HousingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Housing
        fields = ['id', 'title','icon', 'description']
