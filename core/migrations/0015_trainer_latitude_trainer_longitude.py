# Generated by Django 5.1.7 on 2025-04-24 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_formation_city_formation_code_postal_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainer',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='trainer',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
