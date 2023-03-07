from django.db import models
import os

def get_image_path(instance, filename):
    return os.path.join('images', str(instance.id), filename)
# Create your models here.


class City(models.Model):
    name = models.CharField(max_length=100)
    population = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True, upload_to=get_image_path)

    def __str__(self):
        return f"City: {self.name}"
