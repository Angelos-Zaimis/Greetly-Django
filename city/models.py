from django.db import models

# Create your models here.


class City(models.Model):
    name = models.CharField(max_length=100)
    population = models.CharField(max_length=100)

    def __str__(self):
        return f"City: {self.name}"
class ResidencyPermit(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    requirements = models.CharField(max_length=200)

    def __str__(self):
        return f"Permit {self.requirements}"

