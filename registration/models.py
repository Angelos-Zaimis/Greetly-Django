import random

from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model();


def generate_code(length=5):
    numbers = '0123456789'
    return ''.join(random.choice(numbers) for _ in range(length))


class Registration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='registration',default='')
    verification_code = models.IntegerField(default=generate_code)
    email = models.EmailField(default='')
    password = models.CharField(max_length=20, default='')

    def __str__(self):
        return self.user.email