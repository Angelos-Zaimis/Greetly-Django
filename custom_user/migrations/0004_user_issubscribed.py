# Generated by Django 4.1.6 on 2023-09-12 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user', '0003_user_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='isSubscribed',
            field=models.BooleanField(default=False),
        ),
    ]
