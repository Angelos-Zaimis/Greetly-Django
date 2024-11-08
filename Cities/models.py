from django.db import models

CANTON_CHOICES = (
    ('DE', 'German'),
    ('IT', 'Italian'),
    ('FR', 'French'),
)

class City(models.Model):
    name = models.CharField(max_length=100, blank=False)
    image = models.ImageField(upload_to='city_images/', default='', blank=True)
    table_image = models.ImageField(upload_to='city_images/', default='', blank=True)
    canton_region = models.CharField(max_length=20, choices=CANTON_CHOICES, default='')
    cantons_flag = models.ImageField(upload_to='cantons_icons/', default='', blank=True)

    def __str__(self):
        return f"ID: {self.id} Canton: {self.name}"

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=100, default='')
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='city_images/', default='', blank=True)
    table_image = models.ImageField(upload_to='city_image/', default='', blank=True)
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
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    content = models.JSONField(default=dict)  # Set a default value
    image = models.ImageField(upload_to='category_images/', default='', blank=True)
    table_image = models.ImageField(upload_to='city_images/', default='', blank=True)

    def __str__(self):
        return f"ID: {self.id} Information: {self.title} --- {self.subcategory}"
