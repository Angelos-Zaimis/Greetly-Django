import os

from django.db import models

# Create your models here.
from django.db import models
from city.models import City

def get_image_path(instance, filename):
    return os.path.join('images', str(instance.id), filename)
# Create your models here.
class ImmigrationLawsAndRegulations(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE,related_name='ImmigrationLawsAndRegulations')
    title = models.CharField(max_length=200, default='Legal system & immigration')
    titleEs = models.CharField(max_length=200, default='Sistema legal y migración')
    titleGr = models.CharField(max_length=200, default='Νομικό σύστημα και μετανάστευση')
    titleFr = models.CharField(max_length=200, default='Système juridique et immigration')
    titleIt = models.CharField(max_length=200, default='Sistema legale e immigrazione')
    titleGe = models.CharField(max_length=200, default='Rechtssystem und Einwanderung')
    icon = models.ImageField(null=True, blank=True, upload_to=get_image_path)
    description = models.CharField(max_length=200, default='Immigration and legal support,polices')
    descriptionEs = models.CharField(max_length=200, default='Leyes y políticas migratorias')
    descriptionIt = models.CharField(max_length=200, default='Leggi e politiche migratorie')
    descriptionFr = models.CharField(max_length=200, default='Lois et politiques migratoires')
    descriptionGe = models.CharField(max_length=200, default='Migrationsgesetze und -politik')
    descriptionGr = models.CharField(max_length=200, default='Νόμοι και πολιτικές μετανάστευσης')

    def __str__(self):
        return f"Permit {self.title} of {self.city}"

