# Generated by Django 4.1.6 on 2023-07-04 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='country',
            field=models.CharField(default='', max_length=200),
        ),
    ]
