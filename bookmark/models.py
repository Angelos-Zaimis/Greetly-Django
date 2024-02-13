from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class BookMark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks', default='')
    canton = models.CharField(max_length=200, default='', null=False)
    category = models.CharField(max_length=200, default='', null=False)
    title = models.CharField(max_length=200, default='', null=False)
    description = models.CharField(max_length=200, default='', null=False)
    image = models.CharField(max_length=200, default='', null=False)
    table_image = models.CharField(max_length=200, default='', null=False)
    requiredDocuments = ArrayField(models.CharField(max_length=100), blank=True, default=list, null=False)
    saved = models.BooleanField(default=False, null=False)
    uniqueTitle = models.CharField(max_length=200, default='', unique=True, null=False)
