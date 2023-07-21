from rest_framework import serializers
from Translation.models import TranslateImage

class ImageSerializer(serializers.ModelSerializer):
    translatedImage = serializers.ImageField(required=True)  # or serializers.FileField() based on your use case
    target_language = serializers.CharField(required=True)
    class Meta:
        model = TranslateImage
        fields = '__all__'