# Generated by Django 4.2.7 on 2024-11-12 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cities', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='image',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='city',
            name='table_image',
            field=models.CharField(max_length=100),
        ),
    ]
