from rest_framework import serializers
from healthcare.models import HealthCare
class HealthCareSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthCare
        fields = ['id', 'title','titleEs','titleIt','titleFr','titleGr','titleGe','icon',
                  'description','descriptionEs','descriptionIt','descriptionFr','descriptionGe',
                  'descriptionGr',]

