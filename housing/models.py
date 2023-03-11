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
    icon = models.ImageField(null=True, blank=True, upload_to=get_image_path)
    description = models.CharField(max_length=200, default='Finding a place to rent or buy')
    def __str__(self):
        return f"permit {self.title} of {self.city}"

