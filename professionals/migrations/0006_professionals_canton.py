# Generated by Django 4.1.6 on 2024-04-01 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('professionals', '0005_immigrationconsultant'),
    ]

    operations = [
        migrations.AddField(
            model_name='professionals',
            name='canton',
            field=models.CharField(choices=[('AG', 'Aargau'), ('AR', 'Appenzell Ausserrhoden'), ('AI', 'Appenzell Innerrhoden'), ('BL', 'Basel-Landschaft'), ('BS', 'Basel-Stadt'), ('BE', 'Bern'), ('FR', 'Fribourg'), ('GE', 'Geneva'), ('GL', 'Glarus'), ('GR', 'Graubünden'), ('JU', 'Jura'), ('LU', 'Lucerne'), ('NE', 'Neuchâtel'), ('NW', 'Nidwalden'), ('OW', 'Obwalden'), ('SG', 'St. Gallen'), ('SH', 'Schaffhausen'), ('SZ', 'Schwyz'), ('SO', 'Solothurn'), ('TG', 'Thurgau'), ('TI', 'Ticino'), ('UR', 'Uri'), ('VS', 'Valais'), ('VD', 'Vaud'), ('ZG', 'Zug'), ('ZH', 'Zurich')], default='', max_length=20),
        ),
    ]
