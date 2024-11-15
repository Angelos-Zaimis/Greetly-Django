# Generated by Django 4.2.7 on 2024-11-08 14:29

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BookMark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('canton', models.CharField(default='', max_length=200)),
                ('category', models.CharField(default='', max_length=200)),
                ('title', models.CharField(default='', max_length=200)),
                ('description', models.CharField(default='', max_length=200)),
                ('image', models.CharField(default='', max_length=200)),
                ('table_image', models.CharField(default='', max_length=200)),
                ('requiredDocuments', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, default=list, size=None)),
                ('saved', models.BooleanField(default=False)),
                ('uniqueTitle', models.CharField(default='', max_length=200, unique=True)),
            ],
        ),
    ]
