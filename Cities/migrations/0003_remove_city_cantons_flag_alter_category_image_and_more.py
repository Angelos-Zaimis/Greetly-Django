# Generated by Django 4.2.7 on 2024-11-13 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cities', '0002_alter_city_image_alter_city_table_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='cantons_flag',
        ),
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='category',
            name='table_image',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='information',
            name='image',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='information',
            name='table_image',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='image',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='table_image',
            field=models.CharField(max_length=100),
        ),
    ]
