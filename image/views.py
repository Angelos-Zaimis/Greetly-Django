import base64
import io
from django.http import HttpResponse
from django.views import View
from google.cloud import vision
from google.cloud import translate_v2 as translate
from PIL import Image, ImageDraw, ImageFont
from image.serializers import ImageSerializer

class TranslateImageView(View):
    def post(self, request):
        # Deserialize the image data and target language code
        serializer = ImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Retrieve the image and target language from the serializer
        image = serializer.validated_data['image']
        target_language = serializer.validated_data['target_language']

        # Initialize the Google Cloud Vision and Translate clients
        vision_client = vision.ImageAnnotatorClient()
        translate_client = translate.Client()

        # Read the image file
        image_bytes = image.read()

        # Create a Google Cloud Vision image object
        image_vision = vision.Image(content=image_bytes)

        # Detect text from the image
        response = vision_client.text_detection(image=image_vision)
        texts = response.text_annotations
        detected_text = texts[0].description if texts else ''

        # Translate the detected text
        translation = translate_client.translate(detected_text, target_language)

        # Create a new image with the translated text
        image_pil = Image.open(io.BytesIO(image_bytes))
        draw = ImageDraw.Draw(image_pil)
        font = ImageFont.truetype('path/to/your/font.ttf', size=20)  # Path to your desired font file

        # Set the position and color for the translated text
        text_position = (10, 10)
        text_color = (255, 255, 255)  # RGB color

        # Write the translated text on the image
        draw.text(text_position, translation['translatedText'], font=font, fill=text_color)

        # Create a response with the modified image
        response = HttpResponse(content_type='image/jpeg')
        response['Content-Disposition'] = 'attachment; filename="translated_image.jpg"'
        image_pil.save(response, format='JPEG')

        return response

