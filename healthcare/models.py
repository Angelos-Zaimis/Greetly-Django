
# Create your models here.
import os

from django.db import models
from city.models import City

# Create your models here.
def get_image_path(instance, filename):
    return os.path.join('images', str(instance.id), filename)

class HealthCare(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE,related_name='healthcare')
    title = models.CharField(max_length=200, default='Health Care')
    icon = models.ImageField(null=True, blank=True, upload_to=get_image_path)
    description = models.CharField(max_length=200, default='Medical insurance, finding a doctor, mental health')
    def __str__(self):
        return f"permit {self.title} of {self.city}"

