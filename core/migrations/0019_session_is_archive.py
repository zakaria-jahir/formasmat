# Generated by Django 5.1.7 on 2025-04-30 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_session_latitude_session_longitude'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='is_archive',
            field=models.BooleanField(default=False, verbose_name='Archivée'),
        ),
    ]
