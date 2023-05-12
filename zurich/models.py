from django.db import models

# Create your models here.



class Zurich(models.Model):
    name = models.CharField(max_length=200, default='')
