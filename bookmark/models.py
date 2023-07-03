from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.

class BookMark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks', default='')
    canton = models.CharField(max_length=200, default='')
    category = models.CharField(max_length=200, default='')
    title = models.CharField(max_length=200, default='')
    description = models.CharField(max_length=200, default='')
    image = models.CharField(max_length=200, default='')
    requiredDocuments = ArrayField(models.CharField(max_length=100), blank=True, default=list)
    saved = models.BooleanField(default=False)
    uniqueTitle = models.CharField(max_length=200, default='', unique=True)