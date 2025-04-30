from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.urls import reverse
from geopy.geocoders import Nominatim
from django.core.exceptions import ValidationError

def user_photo_path(instance, filename):
    return f'users/{instance.id}/photo/{filename}'

def formation_image_path(instance, filename):
    return f'formations/{instance.code_iperia}/images/{filename}'

def trainer_photo_path(instance, filename):
    """Chemin de stockage pour les photos de formateurs."""
    return f'trainers/{instance.id}/photo/{filename}'

class User(AbstractUser):
    """Utilisateur personnalisé."""
    email = models.EmailField(unique=True, verbose_name="Adresse email")
    is_trainer = models.BooleanField(default=False, verbose_name="Est formateur")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Téléphone")
    address = models.TextField(blank=True, null=True, verbose_name="Adresse")
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ville")
    code_postal = models.CharField(max_length=10, blank=True, null=True, verbose_name="Code postal")
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    # Nouveau champ
    rpe_association = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        verbose_name="RPE ou Association"
    )
    rpe = models.ForeignKey('RPE', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="RPE / Association")
    other_rpe = models.CharField(max_length=255, verbose_name="Autre RPE / Association", blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        
        if self.address and (not self.latitude or not self.longitude):
            try:
                geolocator = Nominatim(user_agent="formation_assmat")
                location = geolocator.geocode(self.address)
                if location:
                    self.latitude = location.latitude
                    self.longitude = location.longitude
            except Exception as e:
                print(f"Erreur de géolocalisation : {e}")
        
        super().save(*args, **kwargs)

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.last_name} {self.first_name}"
        return self.username

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

class Formation(models.Model):
    FORMATION_TYPES = [
        ('initial', 'Formation Initiale'),
        ('continue', 'Formation Continue'),
        ('specialisation', 'Formation Spécialisation'),
    ]

    name = models.CharField(max_length=255, verbose_name="Nom de la formation")
    code_iperia = models.CharField(max_length=50, unique=True, verbose_name="Code IPERIA")
    description = models.TextField(verbose_name="Description")
    duration = models.IntegerField(help_text="Durée en heures", validators=[MinValueValidator(1)], verbose_name="Durée")
    image = models.ImageField(upload_to='formations/images/', null=True, blank=True, verbose_name="Image")
    program_file = models.FileField(upload_to='programs/', null=True, blank=True, verbose_name="Programme détaillé")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de mise à jour")
    type = models.CharField(max_length=20, choices=FORMATION_TYPES, default='initial', verbose_name="Type de formation")
    is_presentiel = models.BooleanField(default=True, verbose_name="Présentiel")
    is_distanciel = models.BooleanField(default=False, verbose_name="Distanciel")
    is_asynchrone = models.BooleanField(default=False, verbose_name="Asynchrone")
    is_active = models.BooleanField(default=True, verbose_name="Formation active")
    city = models.CharField(max_length=100, null=True, blank=True, verbose_name="Ville")
    code_postal = models.CharField(max_length=10, null=True, blank=True, verbose_name="Code postal")
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.code_iperia})"

    def get_absolute_url(self):
        return reverse('core:formation_detail', kwargs={'pk': self.pk})

    def get_modalities_display(self):
        """Retourne une chaîne lisible des modalités."""
        modalities = []
        if self.is_presentiel:
            modalities.append('Présentiel')
        if self.is_distanciel:
            modalities.append('Distanciel')
        if self.is_asynchrone:
            modalities.append('Asynchrone')
        return ', '.join(modalities)

    class Meta:
        verbose_name = "Formation"
        verbose_name_plural = "Formations"
        ordering = ['name']

class Trainer(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Prénom", null=True, blank=True)
    last_name = models.CharField(max_length=100, verbose_name="Nom", null=True, blank=True)
    email = models.EmailField(verbose_name="Email", null=True, blank=True)
    phone = models.CharField(max_length=20, verbose_name="Téléphone", null=True, blank=True)
    bio = models.TextField(blank=True, verbose_name="Biographie")
    photo = models.ImageField(upload_to='trainers/', null=True, blank=True, verbose_name="Photo")
    specialties = models.ManyToManyField('Formation', blank=True, verbose_name="Spécialités")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def get_full_name(self):
        """Retourne le nom complet du formateur."""
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        """Retourne le nom complet du formateur."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        return "Formateur sans nom"

    class Meta:
        verbose_name = "Formateur"
        verbose_name_plural = "Formateurs"
        ordering = ['last_name', 'first_name']

class TrainingRoom(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nom")
    address = models.CharField(max_length=255, verbose_name="Adresse")
    postal_code = models.CharField(max_length=20, verbose_name="Code postal", blank=True, null=True)
    city = models.CharField(max_length=100, verbose_name="Ville", blank=True, null=True)
    capacity = models.IntegerField(validators=[MinValueValidator(1)], verbose_name="Capacité")
    equipment = models.TextField(blank=True, verbose_name="Équipement")
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de mise à jour")
    def __str__(self):
        return f"{self.name} ({self.capacity} places)"
    
class Session(models.Model):
    """Modèle représentant une session de formation."""

    STATUS_CHOICES = [
        ('NON_OUVERTE', 'Non ouverte'),
        ('DEMANDEE', 'Demandée'),
        ('OUVERTE', 'Ouverte'),
        ('COMPLETE', 'Complète'),
        ('PREPAREE', 'Préparée'),
        ('ENVOYEE_FORMATEUR', 'Envoyée formateur'),
        ('ATTENTE_RETOUR', 'En attente retour'),
        ('ATTENTE_TRAITEMENT_SYLVAN', 'En attente traitement Sylvan'),
        ('ATTENTE_TRAITEMENT_IPERIA', 'En attente traitement Ipéria'),
        ('ERREUR_SYLVAN', 'Erreur à traiter Sylvan'),
        ('ERREUR_IPERIA', 'Erreur à traiter Ipéria'),
        ('TERMINEE', 'Terminée'),
    ]

    formation = models.ForeignKey(
        Formation, 
        on_delete=models.CASCADE, 
        related_name='sessions'
    )
    trainers = models.ManyToManyField(
        Trainer, 
        related_name='sessions', 
        blank=True
    )
    status = models.CharField(
        max_length=50, 
        choices=STATUS_CHOICES, 
        default='NON_OUVERTE'
    )
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    iperia_opening_date = models.DateField(null=True, blank=True)
    iperia_deadline = models.DateField(null=True, blank=True)

    address = models.CharField(max_length=255, null=True, blank=True, verbose_name="Adresse")
    city = models.CharField(max_length=100, null=True, blank=True, verbose_name="Ville")
    postal_code = models.CharField(max_length=10, null=True, blank=True, verbose_name="Code postal")

    latitude = models.FloatField(null=True, blank=True, verbose_name="Latitude")
    longitude = models.FloatField(null=True, blank=True, verbose_name="Longitude")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_status_change = models.DateTimeField(default=timezone.now)

    # ✅ Champ pour indiquer si la session est archivée
    is_archive = models.BooleanField(default=False, verbose_name="Archivée")

    def __str__(self):
        return f"{self.formation.name} - {self.start_date or 'Date inconnue'}"


    # Adresse de la session
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name="Adresse")
    city = models.CharField(max_length=100, null=True, blank=True, verbose_name="Ville")
    postal_code = models.CharField(max_length=10, null=True, blank=True, verbose_name="Code postal")

    # ➡️ Coordonnées GPS
    latitude = models.FloatField(null=True, blank=True, verbose_name="Latitude")
    longitude = models.FloatField(null=True, blank=True, verbose_name="Longitude")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_status_change = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.formation.name} - {self.get_status_display()}"
    def save(self, *args, **kwargs):
        # Sauvegarder d'abord la session
        super().save(*args, **kwargs)
        
        # Mettre à jour start_date et end_date à partir des dates de session
        session_dates = self.dates.all()
        if session_dates.exists():
            self.start_date = session_dates.earliest('date').date
            self.end_date = session_dates.latest('date').date
            # Sauvegarder à nouveau sans appeler la méthode save pour éviter une boucle
            Session.objects.filter(pk=self.pk).update(
                start_date=self.start_date, 
                end_date=self.end_date
            )
        
        # Mettre à jour last_status_change à chaque sauvegarde si le statut a changé
        old_status = Session.objects.get(pk=self.pk).status if self.pk else None
        if old_status and old_status != self.status:
            self.last_status_change = timezone.now()
            # Sauvegarder à nouveau sans appeler la méthode save pour éviter une boucle
            Session.objects.filter(pk=self.pk).update(
                last_status_change=self.last_status_change
            )

class SessionDate(models.Model):
    """Modèle représentant une date de session avec sa salle."""
    session = models.ForeignKey(
        Session, 
        on_delete=models.CASCADE, 
        related_name='dates'
    )
    date = models.DateField()
    location = models.ForeignKey(
        TrainingRoom, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='session_dates'
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.session.formation.name} - {self.date}"

class Participant(models.Model):
    FILE_STATUS = [
        ('requested', 'Demandé'),
        ('reminded', 'Relancé'),
        ('electronic_received', 'Dossier reçu électronique'),
        ('paper_received', 'Dossier reçu papier'),
        ('error', 'Dossier en erreur'),
    ]

    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='formation_participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='formations_participants')
    file_status = models.CharField(max_length=20, choices=FILE_STATUS, default='requested')
    comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['session', 'user']
        ordering = ['user__last_name', 'user__first_name']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.session}"

    def get_status_badge_class(self):
        status_classes = {
            'WISH': 'btn-secondary',
            'CONTACTED': 'btn-info',
            'REMINDED': 'btn-warning',
            'FILE_EMAIL': 'btn-primary',
            'FILE_PAPER': 'btn-success',
            'ERROR': 'btn-danger'
        }
        return status_classes.get(self.file_status, 'btn-secondary')

class TrainingWish(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Utilisateur")
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE, verbose_name="Formation")
    session = models.ForeignKey('Session', on_delete=models.SET_NULL, null=True, blank=True, related_name='training_wishes', verbose_name="Session associée")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    notes = models.TextField(blank=True, verbose_name="Notes")

    class Meta:
        verbose_name = "Souhait de formation"
        verbose_name_plural = "Souhaits de formation"
        unique_together = ['user', 'formation']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.formation.name}"

class CompletedTraining(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Utilisateur")
    formation = models.ForeignKey(Formation, on_delete=models.SET_NULL, null=True, verbose_name="Formation")
    completion_date = models.DateField(verbose_name="Date de fin")
    certificate_number = models.CharField(max_length=50, blank=True, verbose_name="Numéro de certificat")
    notes = models.TextField(blank=True, verbose_name="Notes")

    class Meta:
        verbose_name = "Formation complétée"
        verbose_name_plural = "Formations complétées"
        ordering = ['-completion_date']

    def __str__(self):
        return f"{self.user} - {self.formation} ({self.completion_date})"

class SessionParticipant(models.Model):
    """Modèle pour un participant à une session."""
    STATUS_WISH = 'WISH'
    STATUS_CONTACTED = 'CONTACTED'
    STATUS_REMINDED = 'REMINDED'
    STATUS_FILE_RECEIVED_EMAIL = 'FILE_EMAIL'
    STATUS_FILE_RECEIVED_PAPER = 'FILE_PAPER'
    STATUS_ERROR = 'ERROR'

    STATUS_CHOICES = [
        (STATUS_WISH, 'Souhait'),
        (STATUS_CONTACTED, 'Contacté'),
        (STATUS_REMINDED, 'Relancé'),
        (STATUS_FILE_RECEIVED_EMAIL, 'Dossier reçu par email'),
        (STATUS_FILE_RECEIVED_PAPER, 'Dossier reçu papier'),
        (STATUS_ERROR, 'Erreur'),
    ]

    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='session_participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='session_participations')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_WISH)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Participant"
        verbose_name_plural = "Participants"
        ordering = ['created_at']
        unique_together = ['session', 'user']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.session.formation.name}"

    def get_status_badge_class(self):
        """Retourne la classe Bootstrap appropriée pour le badge de statut."""
        status_classes = {
            self.STATUS_WISH: 'bg-info',
            self.STATUS_CONTACTED: 'bg-primary',
            self.STATUS_REMINDED: 'bg-warning',
            self.STATUS_FILE_RECEIVED_EMAIL: 'bg-success',
            self.STATUS_FILE_RECEIVED_PAPER: 'bg-success',
            self.STATUS_ERROR: 'bg-danger',
        }
        return status_classes.get(self.status, 'bg-secondary')

class ParticipantComment(models.Model):
    """Modèle pour les commentaires sur un participant."""
    participant = models.ForeignKey(
        SessionParticipant,
        on_delete=models.CASCADE,
        related_name='participant_comments'  # Changement du related_name
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='authored_comments'  # Changement du related_name
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"
        ordering = ['-created_at']

    def __str__(self):
        return f"Commentaire de {self.author.get_full_name()} sur {self.participant}"

class Notification(models.Model):
    """Modèle de notification pour les utilisateurs."""
    NOTIFICATION_TYPES = (
        ('formation_added', 'Nouvelle formation'),
        ('session_created', 'Session de formation créée'),
        ('wish_assigned', 'Souhait de formation assigné'),
        ('session_reminder', 'Rappel de session'),
        ('session_status_update', 'Mise à jour du statut de session'),
        ('general', 'Information générale'),
    )

    def __init__(self, *args, **kwargs):
        # Convertir title/notification_type s'ils sont présents
        if 'title' in kwargs:
            kwargs['message'] = kwargs.pop('title')
        if 'notification_type' in kwargs:
            kwargs['type'] = kwargs.pop('notification_type')
        super().__init__(*args, **kwargs)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    related_object_id = models.PositiveIntegerField(null=True, blank=True)
    related_object_type = models.CharField(max_length=50, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'

    def __str__(self):
        return f"{self.get_type_display()} - {self.message[:50]}"

    @classmethod
    def create_notification(cls, user, type=None, message=None, related_object=None, **kwargs):
        """Méthode de classe pour créer facilement des notifications."""
        # Permet de passer des arguments supplémentaires
        if 'title' in kwargs:
            message = kwargs['title']
        if 'notification_type' in kwargs:
            type = kwargs['notification_type']

        if not (type and message):
            raise ValueError("Vous devez fournir un type et un message de notification")

        notification = cls(
            user=user,
            type=type,
            message=message,
            related_object_id=related_object.id if related_object else None,
            related_object_type=related_object.__class__.__name__ if related_object else None
        )
        notification.save()
        return notification

    def save(self, *args, **kwargs):
        # Permet de passer title/notification_type et les convertir
        if 'title' in kwargs:
            kwargs['message'] = kwargs.pop('title')
        if 'notification_type' in kwargs:
            kwargs['type'] = kwargs.pop('notification_type')
        
        super().save(*args, **kwargs)

class RPE(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nom du RPE / Association")
    address = models.CharField(max_length=255, verbose_name="Adresse", blank=True, null=True)
    phone = models.CharField(max_length=20, verbose_name="Téléphone", blank=True, null=True)
    email = models.EmailField(verbose_name="Email", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "RPE / Association"
        verbose_name_plural = "RPE / Associations"
        ordering = ['name']

    def __str__(self):
        return self.name
