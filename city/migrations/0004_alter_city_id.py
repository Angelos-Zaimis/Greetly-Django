# Generated by Django 4.1.6 on 2023-03-10 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('city', '0003_alter_city_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]