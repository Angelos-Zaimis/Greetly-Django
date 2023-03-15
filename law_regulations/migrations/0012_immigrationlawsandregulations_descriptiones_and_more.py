# Generated by Django 4.1.6 on 2023-03-15 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('law_regulations', '0011_immigrationlawsandregulations_titlefr_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='immigrationlawsandregulations',
            name='descriptionEs',
            field=models.CharField(default='Leyes y políticas migratorias', max_length=200),
        ),
        migrations.AddField(
            model_name='immigrationlawsandregulations',
            name='descriptionFr',
            field=models.CharField(default='Lois et politiques migratoires', max_length=200),
        ),
        migrations.AddField(
            model_name='immigrationlawsandregulations',
            name='descriptionGe',
            field=models.CharField(default='Migrationsgesetze und -politik', max_length=200),
        ),
        migrations.AddField(
            model_name='immigrationlawsandregulations',
            name='descriptionGr',
            field=models.CharField(default='Νόμοι και πολιτικές μετανάστευσης', max_length=200),
        ),
        migrations.AddField(
            model_name='immigrationlawsandregulations',
            name='descriptionIt',
            field=models.CharField(default='Leggi e politiche migratorie', max_length=200),
        ),
        migrations.AlterField(
            model_name='immigrationlawsandregulations',
            name='description',
            field=models.CharField(default='Immigration and legal support,polices', max_length=200),
        ),
    ]
