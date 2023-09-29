
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.postgres.fields import ArrayField

class City(models.Model):
    name = models.CharField(max_length=100,blank=False)
    image = models.ImageField(upload_to='city_images/', default='', blank=True)
    table_image = models.ImageField(upload_to='city_images/', default='', blank=True)

    def __str__(self):
        return f"ID: {self.id} Canton: {self.name}"

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=100, default='')
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='city_images/', default='', blank=True)
    table_image = models.ImageField(upload_to='city_images/', default='', blank=True)
    icon = models.CharField(max_length=200, default='')

    def __str__(self):
        return f"ID: {self.id} Category: {self.name} --- {self.city}"

class SubCategory(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='category_images/', default='', blank=True)
    table_image = models.ImageField(upload_to='city_images/', default='', blank=True)



    def __str__(self):
        return f"ID: {self.id} Subcategory: {self.title} --- {self.category} "



class Information(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='category_images/', default='', blank=True)
    table_image = models.ImageField(upload_to='city_images/', default='', blank=True)
    requiredDocuments = ArrayField(models.CharField(max_length=100), blank=True, default=list)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f"ID: {self.id} Information: {self.title} --- {self.subcategory}"