
from city.models import City
from rest_framework import serializers

from law_regulations.serializers import ImmigrationLawsAndRegulationsSerializer
from permit.serializers import PermitSerializer
from moneybanking.serializers import MoneyBankingSerializer
from healthcare.serializers import HealthCareSerializer
from employment.serializers import EmploymentSerializer
from housing.serializers import HousingSerializer


class CitySerializer(serializers.ModelSerializer):
    immigrationLawsAndRegulations = ImmigrationLawsAndRegulationsSerializer(many=True, read_only=True, source='ImmigrationLawsAndRegulations')
    permit = PermitSerializer(many=True, read_only=True,source='Permit')
    moneybanking = MoneyBankingSerializer(many=True, read_only=True)
    healthcare = HealthCareSerializer(many=True, read_only=True)
    employment = EmploymentSerializer(many=True, read_only=True)
    housing = HousingSerializer(many=True, read_only=True)
    class Meta:
        model = City
        fields = ['id','name', 'population', 'image','immigrationLawsAndRegulations', 'permit', 'moneybanking',
                  'healthcare', 'employment', 'housing']