# Generated by Django 5.0 on 2024-12-29 02:22

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_sessiondate_options_user_rpe_association'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sessiondate',
            options={},
        ),
        migrations.RemoveField(
            model_name='session',
            name='room',
        ),
        migrations.AddField(
            model_name='formation',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Formation active'),
        ),
        migrations.AlterField(
            model_name='session',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='formation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to='core.formation'),
        ),
        migrations.AlterField(
            model_name='session',
            name='iperia_deadline',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='iperia_opening_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='last_status_change',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='session',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='status',
            field=models.CharField(choices=[('NON_OUVERTE', 'Non ouverte'), ('DEMANDEE', 'Demandée'), ('OUVERTE', 'Ouverte'), ('COMPLETE', 'Complète'), ('PREPAREE', 'Préparée'), ('ENVOYEE_FORMATEUR', 'Envoyée formateur'), ('ATTENTE_RETOUR', 'En attente retour'), ('ATTENTE_TRAITEMENT_SYLVAN', 'En attente traitement Sylvan'), ('ATTENTE_TRAITEMENT_IPERIA', 'En attente traitement Ipéria'), ('ERREUR_SYLVAN', 'Erreur à traiter Sylvan'), ('ERREUR_IPERIA', 'Erreur à traiter Ipéria'), ('TERMINEE', 'Terminée')], default='NON_OUVERTE', max_length=50),
        ),
        migrations.AlterField(
            model_name='session',
            name='trainers',
            field=models.ManyToManyField(blank=True, related_name='sessions', to='core.trainer'),
        ),
        migrations.AlterField(
            model_name='session',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='sessiondate',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='sessiondate',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='sessiondate',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='session_dates', to='core.trainingroom'),
        ),
        migrations.AlterField(
            model_name='sessiondate',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dates', to='core.session'),
        ),
    ]
