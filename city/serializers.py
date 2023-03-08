
from city.models import City
from rest_framework import serializers
class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ['id','name', 'population', 'image']