from django.db import models

# Create your models here.
from django.db import models
from city.models import City
# Create your models here.
class ImmigrationLawsAndRegulations(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE,related_name='ImmigrationLawsAndRegulations')
    title = models.CharField(max_length=200, default='Immigration laws and regulations')


    def __str__(self):
        return f"Permit {self.title} of {self.city}"

