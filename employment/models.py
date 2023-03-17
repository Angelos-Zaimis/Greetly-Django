from django.db import models

# Create your models here.
import os

from django.db import models
from city.models import City

# Create your models here.
def get_image_path(instance, filename):
    return os.path.join('images', str(instance.id), filename)

class Employment(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE,related_name='employment')
    title = models.CharField(max_length=200, default='Employment')
    titleEs = models.CharField(max_length=200, default='Empleo / Trabajo')
    titleIt = models.CharField(max_length=200, default='Impiego / Lavoro')
    titleFr = models.CharField(max_length=200, default='Emploi / Travail')
    titleGr = models.CharField(max_length=200, default='Εργασία / Απασχόληση')
    titleGe = models.CharField(max_length=200, default='Beschäftigung / Arbeit')
    icon = models.ImageField(null=True, blank=True, upload_to=get_image_path)
    description = models.CharField(max_length=200, default='Finding a job, working in Switzerland')
    descriptionEs = models.CharField(max_length=200, default='Encontrar un trabajo / Buscar empleo,Trabajar en Suiza')
    descriptionIt = models.CharField(max_length=200, default='Trovare un lavoro, Lavorare in Svizzera')
    descriptionFr = models.CharField(max_length=200, default='Trouver un emploi, Travailler en Suisse')
    descriptionGr = models.CharField(max_length=200, default='Εύρεση εργασίας, Εργασία στην Ελβετία')
    descriptionGe = models.CharField(max_length=200, default='Einen Job finden, Arbeiten in der Schweiz')
    def __str__(self):
        return f"permit {self.title} of {self.city}"

