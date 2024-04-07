from django.contrib.auth.models import AbstractUser
from django.db import models
import random
import time


def generate_code(length=5):
    random.seed(time.time())  # Seed based on the current time
    numbers = '0123456789'
    return ''.join(random.choice(numbers) for _ in range(length))


def default_product_details():
    return {'subscription_price': '', 'subscription_plan': '', 'subscription_currency': '', 'subscription_id': ''}


ROLE_CHOICES = (
    ('user', 'user'),
    ('businessOwner', 'businessOwner'),
)


class User(AbstractUser):
    is_active = models.BooleanField(default=False)
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
    product_details = models.JSONField(default=default_product_details)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='')

    def __str__(self):
        return f"ID: {self.id} email: {self.email}"
