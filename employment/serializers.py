from rest_framework import serializers
from employment.models import Employment



class EmploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employment
        fields = ['id', 'title','icon', 'description']

