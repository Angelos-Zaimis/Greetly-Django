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
    icon = models.ImageField(null=True, blank=True, upload_to=get_image_path)
    description = models.CharField(max_length=200, default='Immigration and legal support,police')

    def __str__(self):
        return f"Permit {self.title} of {self.city}"

