import os

from django.db import models
from city.models import City

# Create your models here.
def get_image_path(instance, filename):
    return os.path.join('images', str(instance.id), filename)

class Permit(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE,related_name='Permit')
    title = models.CharField(max_length=200, default='Permit')
    icon = models.ImageField(null=True, blank=True, upload_to=get_image_path)
    description = models.CharField(max_length=200, default='Permit process and requirements')
    def __str__(self):
        return f"permit {self.title} of {self.city}"

