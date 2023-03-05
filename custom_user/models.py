from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    first_login = models.BooleanField(default=True)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']



    def __str__(self):
        return f"ID: {self.id} email: {self.email}"