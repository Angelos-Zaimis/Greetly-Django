import os
from rest_framework.views import APIView
from Translation.serializers import ImageSerializer
from django.http import HttpResponse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from PIL import Image, ImageDraw
import io
from google.cloud import vision
from google.cloud import translate_v2 as translate
from google.oauth2 import service_account
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

        imageToTranslate = vision.Image(content=image_bytes)

        # Detect text from the TranslateImage
        response = vision_client.text_detection(image=imageToTranslate)
        print(response)
        texts = response.text_annotations
        detected_text = texts[0].description if texts else ''

        # Translate the detected text
        translation = translate_client.translate(detected_text, target_language)

        # Remove non-ASCII characters that cause encoding errors
        cleaned_translation = ''.join([char if ord(char) < 128 else ' ' for char in translation['translatedText']])

        # Create a new TranslateImage with the translated text
        image_pil = Image.open(io.BytesIO(image_bytes))
        draw = ImageDraw.Draw(image_pil)

        # Set the position and color for the translated text
        text_position = (10, 10)
        text_color = (255, 255, 255)  # RGB color

        # Write the translated text on the image
        draw.text(text_position, cleaned_translation, fill=text_color)

        # Save the translated image to DigitalOcean Spaces
        image_name = 'translated_image.jpg'  # Choose a suitable name for the image
        image_content = image_pil.tobytes()
        image_file = ContentFile(image_content)

        image_path = f'translatedImages/{image_name}'  # Replace 'translatedImages' with your desired folder structure

        default_storage.save(image_path, image_file)

        # Create a response with the URL of the saved image
        response = HttpResponse(content_type='image/jpeg')
        response['Content-Disposition'] = f'attachment; filename="{image_name}"'
        response['X-Space-URL'] = default_storage.url(image_path)

        return response
