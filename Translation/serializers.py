from rest_framework import serializers
from Translation.models import TranslateImage

class ImageSerializer(serializers.ModelSerializer):
    translatedImage = serializers.CharField(required=True)
    target_language = serializers.CharField(required=True)
    class Meta:
        model = TranslateImage
        fields = '__all__'