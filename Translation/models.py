from django.db import models

# Create your models here.
from django.db import models

class TranslateImage(models.Model):
    translatedImage = models.ImageField(upload_to='translatedImages/',blank=False, null=False)