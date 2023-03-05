from django.db import models

# Create your models here.
from django.db import models
from city.models import City
# Create your models here.
class ResidencyPermit(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    requirements = models.CharField(max_length=200)

    def __str__(self):
        return f"Permit {self.requirements}"

