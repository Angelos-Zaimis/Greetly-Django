# Generated by Django 4.1.6 on 2023-04-13 20:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_registration_selectedcitizenship_registration_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registration',
            old_name='selectedCitizenship',
            new_name='selectedCountry',
        ),
    ]
