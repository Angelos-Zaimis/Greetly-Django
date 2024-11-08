import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_login = models.BooleanField(default=True)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']
    is_active = models.BooleanField(default=False)
    selectedCitizenship = models.CharField(max_length=200, default='')
    status = models.CharField(max_length=200, default='')
    country = models.CharField(max_length=200, default='')
    language = models.CharField(max_length=200, null=True, default='en')

    def __str__(self):
        return f"ID: {self.id} email: {self.email}"
