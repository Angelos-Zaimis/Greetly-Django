
from city.models import City
from rest_framework import serializers

from law_regulations.serializers import ImmigrationLawsAndRegulationsSerializer
from permit.serializers import PermitSerializer


class CitySerializer(serializers.ModelSerializer):
    immigrationLawsAndRegulations = ImmigrationLawsAndRegulationsSerializer(many=True, read_only=True, source='ImmigrationLawsAndRegulations')
    permit = PermitSerializer(many=True, read_only=True,source='Permit')

    class Meta:
        model = City
        fields = ['id','name', 'population', 'image','immigrationLawsAndRegulations', 'permit']