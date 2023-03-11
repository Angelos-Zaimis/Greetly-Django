from permit.models import Permit
from rest_framework import serializers

class PermitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permit
        fields = ['id', 'title','icon', 'description']
