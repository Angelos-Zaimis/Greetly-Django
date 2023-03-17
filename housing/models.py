from django.db import models

# Create your models here.
import os

from django.db import models
from city.models import City

# Create your models here.
def get_image_path(instance, filename):
    return os.path.join('images', str(instance.id), filename)

class Housing(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE,related_name='housing')
    title = models.CharField(max_length=200, default='Housing')
    titleEs = models.CharField(max_length=200, default='Vivienda / Alojamiento')
    titleIt = models.CharField(max_length=200, default='Alloggio / Abitazione')
    titleFr = models.CharField(max_length=200, default='Logement / Hébergement')
    titleGr = models.CharField(max_length=200, default='Κατοικία')
    titleGe = models.CharField(max_length=200, default='Wohnen / Unterkunft')
    icon = models.ImageField(null=True, blank=True, upload_to=get_image_path)
    description = models.CharField(max_length=200, default='Finding a place to rent or buy')
    descriptionEs = models.CharField(max_length=200, default='Encontrar un lugar para alquilar o comprar')
    descriptionIt = models.CharField(max_length=200, default='Trovare un posto dove affittare o comprare')
    descriptionFr = models.CharField(max_length=200, default='Trouver un lieu à louer ou acheter')
    descriptionGr = models.CharField(max_length=200, default='Εύρεση καταλύματος προς ενοικίαση ή αγορά ')
    descriptionGe = models.CharField(max_length=200, default='Eine Wohnung oder ein Haus mieten oder kaufen')
    def __str__(self):
        return f"permit {self.title} of {self.city}"

