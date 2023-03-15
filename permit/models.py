import os

from django.db import models
from city.models import City

# Create your models here.
def get_image_path(instance, filename):
    return os.path.join('images', str(instance.id), filename)

class Permit(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE,related_name='Permit')
    title = models.CharField(max_length=200, default='Residence Permit')
    titleEs = models.CharField(max_length=200, default='Permiso de residencia')
    titleIt = models.CharField(max_length=200, default='Permesso di soggiorno')
    titleFr = models.CharField(max_length=200, default='Permis de séjour')
    titleGe = models.CharField(max_length=200, default='Aufenthaltserlaubnis')
    titleGr = models.CharField(max_length=200, default='Άδεια διαμονής')
    icon = models.ImageField(null=True, blank=True, upload_to=get_image_path)
    description = models.CharField(max_length=200, default='Permit process and requirements')
    descriptionEs = models.CharField(max_length=200,
    default='Proceso y requisitos del permiso de residencia')
    descriptionIt = models.CharField(max_length=200,
    default='Processo e requisiti del permesso di soggiorno')
    descriptionFr = models.CharField(max_length=200,
    default='Processus et exigences de permis de séjour')
    descriptionGe = models.CharField(max_length=200,
    default='Verfahren und Anforderungen für die Aufenthaltserlaubnis')
    descriptionGr = models.CharField(max_length=200,
    default='Διαδικασία και απαιτήσεις άδειας διαμονής')
    def __str__(self):
        return f"permit {self.title} of {self.city}"

