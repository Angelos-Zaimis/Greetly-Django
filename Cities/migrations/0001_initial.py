# Generated by Django 4.2.7 on 2024-11-08 14:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(default='', max_length=100)),
                ('image', models.ImageField(blank=True, default='', upload_to='city_images/')),
                ('table_image', models.ImageField(blank=True, default='', upload_to='city_image/')),
                ('icon', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, default='', upload_to='city_images/')),
                ('table_image', models.ImageField(blank=True, default='', upload_to='city_images/')),
                ('canton_region', models.CharField(choices=[('DE', 'German'), ('IT', 'Italian'), ('FR', 'French')], default='', max_length=20)),
                ('cantons_flag', models.ImageField(blank=True, default='', upload_to='cantons_icons/')),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, default='', upload_to='category_images/')),
                ('table_image', models.ImageField(blank=True, default='', upload_to='city_images/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Cities.category')),
            ],
        ),
        migrations.CreateModel(
            name='Information',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('subtitle', models.CharField(default='', max_length=100)),
                ('content', models.JSONField(default=dict)),
                ('image', models.ImageField(blank=True, default='', upload_to='category_images/')),
                ('table_image', models.ImageField(blank=True, default='', upload_to='city_images/')),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Cities.subcategory')),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Cities.city'),
        ),
    ]
