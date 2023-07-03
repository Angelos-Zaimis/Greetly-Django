from django.contrib.postgres.fields import ArrayField
from django.db import models


# Create your models here.


class TeamMembers(models.Model):
    profileImage = models.ImageField(upload_to='profileImages/', default='', blank=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=200, default='')
    location = models.CharField(default='', max_length=200)
    occupation = models.CharField(max_length=200, default='')
    languageOne = models.ImageField(upload_to='languages/', default='', blank=True)
    languageTwo = models.ImageField(upload_to='languages/', default='', blank=True)
    languageThree = models.ImageField(upload_to='languages/', default='', blank=True)
    languageFour = models.ImageField(upload_to='languages/', default='', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'teamMembers'
