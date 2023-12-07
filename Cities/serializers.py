from rest_framework import serializers
from Cities.models import City,Category,SubCategory,Information, Steps, Location
from rest_framework import serializers

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'




class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'

class InformationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Information
        fields = '__all__'

