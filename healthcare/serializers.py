from rest_framework import serializers
from healthcare.models import HealthCare
class HealthCareSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthCare
        fields = ['id', 'title','icon', 'description']

