from rest_framework import serializers
from bookmark.models import BookMark


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookMark
        fields = '__all__'


class BookmarkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookMark
        fields = '__all__'
