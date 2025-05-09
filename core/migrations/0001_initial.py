# Generated by Django 5.0 on 2024-12-28 21:53

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Formation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nom de la formation')),
                ('code_iperia', models.CharField(max_length=50, unique=True, verbose_name='Code IPERIA')),
                ('description', models.TextField(verbose_name='Description')),
                ('duration', models.IntegerField(help_text='Durée en heures', validators=[django.core.validators.MinValueValidator(1)], verbose_name='Durée')),
                ('image', models.ImageField(blank=True, null=True, upload_to='formations/', verbose_name='Image')),
                ('program_file', models.FileField(blank=True, null=True, upload_to='programs/', verbose_name='Programme détaillé')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de mise à jour')),
            ],
            options={
                'verbose_name': 'Formation',
                'verbose_name_plural': 'Formations',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='FormationModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('duration', models.IntegerField(help_text='Durée en heures')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TrainerNew',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='', max_length=100, verbose_name='Prénom')),
                ('last_name', models.CharField(default='', max_length=100, verbose_name='Nom')),
                ('email', models.EmailField(default='no-email@example.com', max_length=254, verbose_name='Email')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Téléphone')),
                ('specialties', models.TextField(blank=True, null=True, verbose_name='Spécialités')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Formateur',
                'verbose_name_plural': 'Formateurs',
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.CreateModel(
            name='TrainingRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nom')),
                ('address', models.CharField(max_length=255, verbose_name='Adresse')),
                ('capacity', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Capacité')),
                ('equipment', models.TextField(blank=True, verbose_name='Équipement')),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de mise à jour')),
            ],
            options={
                'verbose_name': 'Salle de formation',
                'verbose_name_plural': 'Salles de formation',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Adresse email')),
                ('is_trainer', models.BooleanField(default=False, verbose_name='Est formateur')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Téléphone')),
                ('address', models.TextField(blank=True, null=True, verbose_name='Adresse')),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Utilisateur',
                'verbose_name_plural': 'Utilisateurs',
                'ordering': ['last_name', 'first_name'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='CompletedTraining',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completion_date', models.DateField(verbose_name='Date de fin')),
                ('certificate_number', models.CharField(blank=True, max_length=50, verbose_name='Numéro de certificat')),
                ('notes', models.TextField(blank=True, verbose_name='Notes')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur')),
                ('formation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.formation', verbose_name='Formation')),
            ],
            options={
                'verbose_name': 'Formation complétée',
                'verbose_name_plural': 'Formations complétées',
                'ordering': ['-completion_date'],
            },
        ),
        migrations.CreateModel(
            name='ParticipantModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'En attente'), ('confirmed', 'Confirmé'), ('cancelled', 'Annulé'), ('completed', 'Terminé')], default='pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ParticipantCommentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='core.participantmodel')),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PENDING', 'En attente'), ('OPEN', 'Ouverte'), ('VALIDATED', 'Validée'), ('COMPLETED', 'Terminée'), ('ARCHIVED', 'Archivée'), ('CANCELLED', 'Annulée')], default='PENDING', max_length=20, verbose_name='Statut')),
                ('iperia_opening_date', models.DateField(blank=True, null=True, verbose_name="Date d'ouverture Ipéria")),
                ('iperia_deadline', models.DateField(blank=True, null=True, verbose_name='Date limite Ipéria')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Dernière modification')),
                ('last_status_change', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Dernier changement de statut')),
                ('formation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.formation', verbose_name='Formation')),
                ('trainers', models.ManyToManyField(related_name='sessions', to=settings.AUTH_USER_MODEL, verbose_name='Formateurs')),
            ],
            options={
                'verbose_name': 'Session',
                'verbose_name_plural': 'Sessions',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='SessionComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='session_comments', to=settings.AUTH_USER_MODEL)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='core.session')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='SessionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('draft', 'Brouillon'), ('published', 'Publiée'), ('in_progress', 'En cours'), ('completed', 'Terminée'), ('cancelled', 'Annulée')], default='draft', max_length=20)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('max_participants', models.IntegerField(default=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('formation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to='core.formationmodel')),
            ],
        ),
        migrations.AddField(
            model_name='participantmodel',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='core.sessionmodel'),
        ),
        migrations.CreateModel(
            name='SessionParticipant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('WISH', 'Souhait'), ('CONTACTED', 'Contacté'), ('REMINDED', 'Relancé'), ('FILE_EMAIL', 'Dossier reçu par email'), ('FILE_PAPER', 'Dossier reçu papier'), ('ERROR', 'Erreur')], default='WISH', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='session_participants', to='core.session')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='session_participations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Participant',
                'verbose_name_plural': 'Participants',
                'ordering': ['created_at'],
                'unique_together': {('session', 'user')},
            },
        ),
        migrations.CreateModel(
            name='ParticipantComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='participant_comments', to=settings.AUTH_USER_MODEL)),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='core.sessionparticipant')),
            ],
            options={
                'verbose_name': 'Commentaire',
                'verbose_name_plural': 'Commentaires',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='TrainerModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('bio', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('specialties', models.ManyToManyField(related_name='trainers', to='core.formationmodel')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='sessionmodel',
            name='trainer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sessions', to='core.trainermodel'),
        ),
        migrations.CreateModel(
            name='SessionDate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Date')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dates', to='core.session', verbose_name='Session')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.trainingroom', verbose_name='Lieu')),
            ],
            options={
                'verbose_name': 'Date de session',
                'verbose_name_plural': 'Dates de session',
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='TrainingWishModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'En attente'), ('assigned', 'Assigné'), ('cancelled', 'Annulé')], default='pending', max_length=20)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('formation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.formationmodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_status', models.CharField(choices=[('requested', 'Demandé'), ('reminded', 'Relancé'), ('electronic_received', 'Dossier reçu électronique'), ('paper_received', 'Dossier reçu papier'), ('error', 'Dossier en erreur')], default='requested', max_length=20)),
                ('comments', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='formations_participants', to=settings.AUTH_USER_MODEL)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='formation_participants', to='core.session')),
            ],
            options={
                'ordering': ['user__last_name', 'user__first_name'],
                'unique_together': {('session', 'user')},
            },
        ),
        migrations.CreateModel(
            name='TrainingWish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('notes', models.TextField(blank=True, verbose_name='Notes')),
                ('formation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.formation', verbose_name='Formation')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur')),
            ],
            options={
                'verbose_name': 'Souhait de formation',
                'verbose_name_plural': 'Souhaits de formation',
                'ordering': ['-created_at'],
                'unique_together': {('user', 'formation')},
            },
        ),
    ]
