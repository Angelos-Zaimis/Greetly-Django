from django.db import models

# Create your models here.
import os

from django.db import models
from city.models import City

# Create your models here.
def get_image_path(instance, filename):
    return os.path.join('images', str(instance.id), filename)

class MoneyBanking(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE,related_name='moneybanking')
    title = models.CharField(max_length=200, default='Money & banking')
    titleEs = models.CharField(max_length=200, default='Dinero y banca')
    titleIt = models.CharField(max_length=200, default='Moneta e banca')
    titleFr = models.CharField(max_length=200, default='Argent et banque')
    titleGr = models.CharField(max_length=200, default='Χρήματα και τραπεζικό σύστημα')
    titleGe = models.CharField(max_length=200, default='Geld und Bankwesen')
    icon = models.ImageField(null=True, blank=True, upload_to=get_image_path)
    description = models.CharField(max_length=200, default='Opening a bank account,filing taxes')
    descriptionEs = models.CharField(max_length=200, default='Apertura de una cuenta bancaria,Presentación de impuestos')
    descriptionIt = models.CharField(max_length=200, default='Apertura di un conto bancario,Presentazione della dichiarazione dei redditi')
    descriptionFr = models.CharField(max_length=200, default='Ouverture d un compte bancaire,Déclaration fiscale')
    descriptionGr = models.CharField(max_length=200, default='Άνοιγμα τραπεζικού λογαριασμού,Υποβολή φορολογικής δήλωσης')
    descriptionGe = models.CharField(max_length=200, default='Eröffnung eines Bankkontos,Einreichung der Steuererklärung')
    def __str__(self):
        return f"permit {self.title} of {self.city}"

