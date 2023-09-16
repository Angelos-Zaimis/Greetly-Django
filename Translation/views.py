
import base64
import io
import json
import os
from PIL import Image, ImageDraw, ImageFont

from django.http import HttpResponse
from django.views import View
from google.auth.credentials import AnonymousCredentials
from google.cloud import vision
from google.cloud import translate_v2 as translate
from PIL import Image, ImageDraw, ImageFont
from rest_framework.views import APIView
from google.oauth2 import service_account
from Translation.serializers import ImageSerializer


class TranslateImageView(APIView):
    def post(self, request):
        # Deserialize the TranslateImage data and target language code
        serializer = ImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Retrieve the TranslateImage and target language from the serializer
        image = serializer.validated_data['translatedImage']
        target_language = serializer.validated_data['target_language']

        key_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

        # Initialize the Google Cloud Vision and Translate clients
        if key_path is None:
            print("Environment variable GOOGLE_APPLICATION_CREDENTIALS is not set.")
        elif not os.path.isfile(key_path):
            print(f"File does not exist at path: {key_path}")
        else:
            print(f"File exists at path: {key_path}")
        credentials = service_account.Credentials.from_service_account_file(key_path)

        # Initialize the Google Cloud Vision and Translate clients
        vision_client = vision.ImageAnnotatorClient(credentials=credentials)
        translate_client = translate.Client(credentials=credentials)
        # Read the TranslateImage file
        image_bytes = image.read()

        imageToTranslate= vision.Image(content=image_bytes)
        # Detect text from the TranslateImage
        response = vision_client.text_detection(image=imageToTranslate)
        print(response)
        texts = response.text_annotations
        detected_text = texts[0].description if texts else ''

        # Translate the detected text
        translation = translate_client.translate(detected_text, target_language)

        # Create a new TranslateImage with the translated text
        image_pil = Image.open(io.BytesIO(image_bytes))
        draw = ImageDraw.Draw(image_pil)
        font = ImageFont.load_default()
        # Set the position and color for the translated text
        text_position = (10, 10)
        text_color = (255, 255, 255)  # RGB color

        # Write the translated text on the TranslateImage
        draw.text(text_position, translation['translatedText'], font=font, fill=text_color)

        # Create a response with the modified TranslateImage
        response = HttpResponse(content_type='TranslateImage/jpeg')
        response['Content-Disposition'] = 'attachment; filename="translated_image.jpg"'
        image_pil.save(response, format='JPEG')

        return response
