from django.http import JsonResponse
from django.core.files.base import ContentFile
from .forms import ImageForm
from .models import Image
from .utils import detect_text_and_positions, translate_text, overlay_text_on_image
from google.cloud import translate_v2 as translate

def upload_and_translate(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save()
            target_language = request.POST.get('target_language', 'en')
            translator_client = translate.Client()
            detected_texts = detect_text_and_positions(image_instance.picture.path)
            translated_texts = []

            for text_info in detected_texts:
                translated_text = translate_text(text_info['text'], target_language, translator_client)
                translated_texts.append({
                    'translatedText': translated_text,
                    'boundingBox': text_info['boundingBox']
                })

            # Specify the path to your font file
            modified_img_bytes = overlay_text_on_image(image_instance.picture.path, translated_texts)
            image_instance.picture.save(image_instance.picture.name, ContentFile(modified_img_bytes), save=True)

            full_image_url = request.build_absolute_uri(image_instance.picture.url)
            return JsonResponse({'image_url': full_image_url})
        else:
            return JsonResponse({'error': 'The submitted file is empty'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
