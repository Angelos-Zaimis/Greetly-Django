from urllib.parse import urljoin

from django.contrib.sites.shortcuts import get_current_site

from Cities.models import City, Category, SubCategory, Information
from rest_framework import serializers


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request is not None:
            base_url = request.build_absolute_uri('/')
            for field in ['image', 'cantons_flag', 'table_image']:
                if representation[field] and not representation[field].startswith(('http://', 'https://')):
                    representation[field] = base_url + representation[field][1:]
        return representation


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
