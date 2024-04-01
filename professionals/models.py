from django.db import models

CANTON_CHOICES = (
    ('AG', 'Aargau'),
    ('AR', 'Appenzell Ausserrhoden'),
    ('AI', 'Appenzell Innerrhoden'),
    ('BL', 'Basel-Landschaft'),
    ('BS', 'Basel-Stadt'),
    ('BE', 'Bern'),
    ('FR', 'Fribourg'),
    ('GE', 'Geneva'),
    ('GL', 'Glarus'),
    ('GR', 'Graubünden'),
    ('JU', 'Jura'),
    ('LU', 'Lucerne'),
    ('NE', 'Neuchâtel'),
    ('NW', 'Nidwalden'),
    ('OW', 'Obwalden'),
    ('SG', 'St. Gallen'),
    ('SH', 'Schaffhausen'),
    ('SZ', 'Schwyz'),
    ('SO', 'Solothurn'),
    ('TG', 'Thurgau'),
    ('TI', 'Ticino'),
    ('UR', 'Uri'),
    ('VS', 'Valais'),
    ('VD', 'Vaud'),
    ('ZG', 'Zug'),
    ('ZH', 'Zurich'),
)



class Professionals(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=200, default='')
    profileImage = models.ImageField(upload_to='profileImages/', blank=True)
    languages = models.JSONField(default=list, blank=True)
    review = models.IntegerField(default=0)
    type = models.CharField(max_length=50, blank=True)
    latitude = models.CharField(max_length=50, blank=True)
    longitude = models.CharField(max_length=50, blank=True)
    latitudeDelta = models.CharField(max_length=50, blank=True)
    longitudeDelta = models.CharField(max_length=50, blank=True)
    linkAddress = models.CharField(max_length=50, blank=True)
    canton = models.CharField(max_length=20, choices=CANTON_CHOICES, default='')

    def __str__(self):
        return self.name


class InsuranceAgent(Professionals):
    occupation = models.CharField(max_length=200, default='')
    licensed = models.BooleanField(default=False)
    location = models.CharField(default='', max_length=200)
    specialization = models.CharField(default='', max_length=500)
    aboutMe = models.CharField(default='', max_length=500)

    def save(self, *args, **kwargs):
        self.type = 'InsuranceAgent'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.occupation} - {self.name}"


class ImmigrationConsultant(Professionals):
    occupation = models.CharField(max_length=200, default='')
    licensed = models.BooleanField(default=False)
    location = models.CharField(default='', max_length=200)
    specialization = models.CharField(default='', max_length=500)
    aboutMe = models.CharField(default='', max_length=500)

    def save(self, *args, **kwargs):
        self.type = 'ImmigrationConsultant'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.occupation} - {self.name}"
