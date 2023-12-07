from django.contrib import admin
from Cities.models import City,SubCategory,Category, Information, Steps, Location
# Register your models here.

admin.site.register(City)
admin.site.register(SubCategory)
admin.site.register(Category)
admin.site.register(Information)