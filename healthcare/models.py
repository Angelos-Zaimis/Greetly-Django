
# Create your models here.
import os

from django.db import models
from city.models import City

# Create your models here.
def get_image_path(instance, filename):
    return os.path.join('images', str(instance.id), filename)

class HealthCare(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE,related_name='healthcare')
    title = models.CharField(max_length=200, default='Health Care')
    titleEs = models.CharField(max_length=200, default='Atención médica')
    titleIt = models.CharField(max_length=200, default='Assistenza sanitaria')
    titleFr = models.CharField(max_length=200, default='Soins de santé')
    titleGr = models.CharField(max_length=200, default='Φροντίδα & υγεία')
    titleGe = models.CharField(max_length=200, default='Gesundheitsversorgung')
    icon = models.ImageField(null=True, blank=True, upload_to=get_image_path)
    description = models.CharField(max_length=200, default='Medical insurance, finding a doctor, mental health')
    descriptionEs = models.CharField(max_length=200, default='Seguro médico, Encontrar un médico, Salud mental')
    descriptionIt = models.CharField(max_length=200, default='Assicurazione sanitaria, Trovare un medico, Salute mentale')
    descriptionFr = models.CharField(max_length=200, default='Assurance maladie, Trouver un médecin, Santé mentale')
    descriptionGr = models.CharField(max_length=200, default='Ιατρική ασφάλεια, Εύρεση γιατρού, Ψυχική υγεία')
    descriptionGe = models.CharField(max_length=200, default='Krankenversicherung, Einen Arzt finden, Psychische Gesundheit')
    def __str__(self):
        return f"permit {self.title} of {self.city}"

