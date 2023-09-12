import random
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

def generate_code(length=5):
    numbers = '0123456789'
    return ''.join(random.choice(numbers) for _ in range(length))


class User(AbstractUser):
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    first_login = models.BooleanField(default=True)
    isSubscribed = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']
    selectedCitizenship = models.CharField(max_length=200, default='')
    status = models.CharField(max_length=200, default='')
    country = models.CharField(max_length=200, default='')
    language = models.CharField(max_length=200, null=True, default='en')
    code = models.IntegerField(default=generate_code)

    def __str__(self):
        return f"ID: {self.id} email: {self.email}"
