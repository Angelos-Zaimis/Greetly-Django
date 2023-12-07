
from django.db import migrations, models

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Cities', '0007_city_canton_region_alter_category_table_image'),
    ]

    operations = [

        migrations.CreateModel(
            name='Information',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('subtitle', models.CharField(default='', max_length=100)),
                ('description', models.CharField(max_length=1000)),
                ('image', models.ImageField(blank=True, default='', upload_to='category_images/')),
                ('requiredDocuments', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, default=list, size=None)),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Cities.subcategory')),
            ],
        ),
    ]

