from django.db import models
from city.models import City

# Create your models here.


class Permit(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default='Permit process and requirements')

    def __str__(self):
        return f"Permit {self.title} of {self.city}"

