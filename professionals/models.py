from django.db import models

from professionals.cantons import CANTON_CHOICES


class Professionals(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=200, default='')
    profileImage = models.ImageField(upload_to='profileImages/', blank=True)
    languages = models.JSONField(default=list, blank=True)
    review = models.IntegerField(default=0)
    type = models.CharField(max_length=50, blank=True)
    latitude = models.CharField(max_length=50, blank=True)
    longitude = models.CharField(max_length=50, blank=True)
    latitudeDelta = models.CharField(max_length=50, blank=True)
    longitudeDelta = models.CharField(max_length=50, blank=True)
    linkAddress = models.CharField(max_length=50, blank=True)
    canton = models.CharField(max_length=20, choices=CANTON_CHOICES, default='')

    def __str__(self):
        return self.name

class InsuranceAgent(Professionals):
    occupation = models.CharField(max_length=200, default='')
    licensed = models.BooleanField(default=False)
    location = models.CharField(default='', max_length=200)
    specialization = models.CharField(default='', max_length=500)
    aboutMe = models.CharField(default='', max_length=500)

    def save(self, *args, **kwargs):
        self.type = 'InsuranceAgent'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.occupation} - {self.name}"

class ImmigrationConsultant(Professionals):
    occupation = models.CharField(max_length=200, default='')
    licensed = models.BooleanField(default=False)
    location = models.CharField(default='', max_length=200)
    specialization = models.CharField(default='', max_length=500)
    aboutMe = models.CharField(default='', max_length=500)

    def save(self, *args, **kwargs):
        self.type = 'ImmigrationConsultant'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.occupation} - {self.name}"
