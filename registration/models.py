import random
import time
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


def generate_code(length=5):
    random.seed(time.time())
    numbers = '0123456789'
    return ''.join(random.choice(numbers) for _ in range(length))


class Registration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='registration', default='')
    verification_code = models.IntegerField(default=generate_code)
    email = models.EmailField(default='')
    password = models.CharField(max_length=20, default='')
    selectedCountry = models.CharField(max_length=200, default='')
    status = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.email
