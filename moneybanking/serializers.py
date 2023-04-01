

from moneybanking.models import MoneyBanking
from rest_framework import serializers

class MoneyBankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoneyBanking
        fields = ['id', 'title','titleEs','titleIt', 'titleFr','titleGr','titleGe','icon', 'description',
                  'descriptionEs','descriptionIt','descriptionFr','descriptionGr','descriptionGe']