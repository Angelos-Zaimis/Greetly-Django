from rest_framework import serializers
from bookmark.models import BookMark

class BookmakrkSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookMark
        fields = '__all__'

class BookmakrkCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookMark
        fields = '__all__'

