from rest_framework import serializers
from law_regulations.models import ImmigrationLawsAndRegulations

class ImmigrationLawsAndRegulationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImmigrationLawsAndRegulations
        fields = ['id', 'title','icon','titleEs', 'titleGr','titleFr',
                  'titleIt', 'titleGe','description','descriptionEs', 'descriptionIt','descriptionFr',
                  'descriptionGr', 'descriptionGe']

