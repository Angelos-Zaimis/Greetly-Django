from google.cloud import vision
from google.cloud import translate_v2 as translate
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO


def detect_text_and_positions(image_path):
    client = vision.ImageAnnotatorClient()
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    response = client.text_detection(image=image)

    annotations = response.text_annotations

    translations = []
    for annotation in annotations[1:]:
        description = annotation.description
        vertices = [{'x': vertex.x, 'y': vertex.y} for vertex in annotation.bounding_poly.vertices]
        translations.append({'text': description, 'boundingBox': vertices})

    return translations

def estimate_background_color(image_path, bounding_box):
    with Image.open(image_path) as img:
        # Sample pixels around the bounding box
        pixels = []
        for x in range(bounding_box[0]['x'], bounding_box[1]['x']):
            for y in range(bounding_box[0]['y'] - 10, bounding_box[0]['y']):  # Sample above the text
                pixels.append(img.getpixel((x, y)))
            for y in range(bounding_box[2]['y'], bounding_box[2]['y'] + 10):  # Sample below the text
                pixels.append(img.getpixel((x, y)))

        # Find the most common pixel value
        most_common_color = max(set(pixels), key=pixels.count)
        return most_common_color
def translate_text(text, target_language, translator_client):
    result = translator_client.translate(text, target_language=target_language)
    return result['translatedText']






def get_approximate_font_size(target_height):
    # This function approximates font size based on the target height.
    # The factor '0.75' is an arbitrary value that works for the default PIL font. Adjust as needed.
    return int(target_height * 0.75)
def overlay_text_on_image(image_path, translations):
    with Image.open(image_path) as img:
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()  # Use PIL's default font

        for translation in translations:
            text = translation['translatedText']
            vertices = translation['boundingBox']

            # Estimate background color
            background_color = estimate_background_color(image_path, vertices)

            # Calculate bounding box height and estimate font size
            bounding_box_height = vertices[3]['y'] - vertices[0]['y']
            font_size = get_approximate_font_size(bounding_box_height)

            # Obscure the original text with the background color
            draw.rectangle([vertices[0]['x'], vertices[0]['y'], vertices[2]['x'], vertices[2]['y']], fill=background_color)

            # Overlay the translated text
            # Note: The default font does not support changing size, so we're using an approximation
            draw.text((vertices[0]['x'], vertices[0]['y']), text, fill="black", font=font, )

        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format=img.format)
        img_byte_arr = img_byte_arr.getvalue()
        return img_byte_arr