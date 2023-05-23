from django.db import models

# Create your models here.
from django.db import models
from rest_framework.response import Response
from rest_framework.views import APIView


class City(models.Model):
    name = models.CharField(max_length=100,blank=False)
    image = models.ImageField(upload_to='city_images/', default='', blank=True)

    def __str__(self):
        return f"ID: {self.id} Name: {self.name}"

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, default='')
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='category_images/', default='', blank=True)
    def __str__(self):
        return f"ID: {self.id} Category: {self.name} --- {self.city}"

class Information(models.Model):
    title = models.CharField(max_length=100)
    name = models.CharField(max_length=100, default='')
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"ID: {self.id} Name: {self.title} --- {self.category} "


