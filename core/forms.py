from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import Formation, Trainer, TrainingRoom, TrainingWish, Session, SessionDate, RPE

User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    """Formulaire d'inscription utilisateur."""

    username = forms.CharField(
        required=True,
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Choisissez un nom d'utilisateur"
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'exemple@email.com',
            'autocomplete': 'username'
        })
    )
    first_name = forms.CharField(
        required=True,
        label="Prénom",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'autocomplete': 'given-name'
        })
    )
    last_name = forms.CharField(
        required=True,
        label="Nom",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'autocomplete': 'family-name'
        })
    )
    phone = forms.CharField(
        required=True,
        label="Téléphone",
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'autocomplete': 'tel',
            'placeholder': "0712121212",
            'id': 'id_phone',
            'pattern': '[0-9]{10}'
        })
    )
    city = forms.CharField(
        required=True,
        label="Ville",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex. : La Rochelle'
        })
    )
    code_postal = forms.CharField(
        required=True,
        label="Code postal",
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex. : 17000'
        })
    )
    address = forms.CharField(
        required=True,
        label="Adresse",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'autocomplete': 'street-address'
        })
    )
    rpe = forms.ModelChoiceField(
        queryset=RPE.objects.all(),
        required=False,
        label="RPE / Association",
        empty_label="Sélectionnez votre RPE / Association"
    )
    other_rpe = forms.CharField(
        required=False,
        label="Autre RPE / Association",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'style': 'display: none;'
        })
    )

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'phone', 'city', 'code_postal', 'address',
            'rpe', 'other_rpe', 'password1', 'password2'
        ]
class UserProfileForm(forms.ModelForm):
    """Formulaire de profil utilisateur."""
    rpe = forms.ModelChoiceField(
        queryset=RPE.objects.all().order_by('name'),
        required=False,
        label="RPE / Association",
        empty_label="Sélectionnez votre RPE / Association"
    )
    other_rpe = forms.CharField(
        required=False,
        label="Autre RPE / Association",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'rpe', 'other_rpe']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class FormationForm(forms.ModelForm):
    class Meta:
        model = Formation
        fields = [
            'name', 'code_iperia', 'description', 'duration',
            'image', 'program_file', 'type',
            'is_presentiel', 'is_distanciel', 'is_asynchrone',
            'city', 'code_postal'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code_iperia': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'code_postal': forms.TextInput(attrs={'class': 'form-control'}),
        }

class TrainingRoomForm(forms.ModelForm):
    class Meta:
        model = TrainingRoom
        fields = ['name', 'address', 'capacity', 'equipment']
        widgets = {
            'equipment': forms.Textarea(attrs={'rows': 4}),
        }

class TrainerForm(forms.ModelForm):
    class Meta:
        model = Trainer
        fields = ['first_name', 'last_name', 'email', 'phone', 'specialties', 'bio', 'photo']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'specialties': forms.SelectMultiple(attrs={'class': 'form-select', 'multiple': 'multiple'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        help_texts = {
            'first_name': 'Prénom du formateur',
            'last_name': 'Nom du formateur',
            'email': 'Email professionnel du formateur',
            'phone': 'Numéro de téléphone (optionnel)',
            'specialties': 'Formations sur lesquelles le formateur intervient',
            'bio': 'Courte biographie du formateur',
            'photo': 'Photo du formateur (optionnelle)'
        }

class TrainingWishForm(forms.ModelForm):
    formation = forms.ModelChoiceField(
        queryset=Formation.objects.filter(is_active=True),  # Filtrer uniquement les formations actives
        label="Formation",
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Sélectionnez une formation"
    )

    class Meta:
        model = TrainingWish
        fields = ['formation', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class SessionDateForm(forms.ModelForm):
    """Formulaire pour les dates de session avec salle optionnelle."""
    location = forms.ModelChoiceField(
        queryset=TrainingRoom.objects.all(), 
        required=False, 
        label="Salle",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = SessionDate
        fields = ['date', 'location']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class SessionForm(forms.ModelForm):
    """Version minimale du formulaire de session pour la compatibilité."""
    class Meta:
        model = Session
        fields = ['formation', 'status', 'iperia_opening_date', 'iperia_deadline']
        widgets = {
            'formation': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'iperia_opening_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'iperia_deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        }

class CustomSessionForm(forms.Form):
    """Formulaire personnalisé pour la création de session."""
    
    # Champs de base de la session
    formation = forms.ModelChoiceField(
        queryset=Formation.objects.filter(is_active=True),  # Filtrer uniquement les formations actives
        label="Formation",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    status = forms.ChoiceField(
        choices=Session.STATUS_CHOICES, 
        label="Statut de la session",
        widget=forms.Select(attrs={'class': 'form-select'}),
        initial='PENDING'
    )
    
    iperia_opening_date = forms.DateField(
        label="Date d'ouverture Ipéria",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=False
    )
    
    iperia_deadline = forms.DateField(
        label="Date limite Ipéria",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=False
    )
    
    # Sélection des formateurs
    trainers = forms.ModelMultipleChoiceField(
        queryset=Trainer.objects.filter(
            first_name__isnull=False, 
            last_name__isnull=False
        ).exclude(first_name='', last_name=''),
        label="Formateurs",
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}),
        required=False
    )
    
    # Champs dynamiques pour les dates et salles
    date_count = forms.IntegerField(
        widget=forms.HiddenInput(), 
        initial=0
    )
    
    def __init__(self, *args, **kwargs):
        print("Initialisation du formulaire de session")
        super().__init__(*args, **kwargs)
        
        # Personnaliser l'affichage des formateurs
        self.fields['trainers'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name}"
        
        # Ajouter des champs dynamiques pour les dates et salles
        for i in range(5):  # Permettre jusqu'à 5 dates
            self.fields[f'date_{i}'] = forms.DateField(
                label=f"Date {i+1}",
                widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                required=False
            )
            
            self.fields[f'room_{i}'] = forms.ModelChoiceField(
                queryset=TrainingRoom.objects.all(),
                label=f"Salle pour la date {i+1}",
                widget=forms.Select(attrs={'class': 'form-select'}),
                required=False
            )
        print("Formulaire de session initialisé avec succès")
    
    def clean(self):
        cleaned_data = super().clean()
        rpe = cleaned_data.get("rpe")
        other_rpe = cleaned_data.get("other_rpe")

        if not rpe and not other_rpe:
            raise forms.ValidationError("Veuillez sélectionner un RPE ou en indiquer un autre.")

        return cleaned_data

    def save(self):
        """Enregistrer la session et ses dates."""
        # Créer la session
        session = Session.objects.create(
            formation=self.cleaned_data['formation'],
            status=self.cleaned_data['status'],
            iperia_opening_date=self.cleaned_data.get('iperia_opening_date'),
            iperia_deadline=self.cleaned_data.get('iperia_deadline')
        )
        
        # Ajouter les formateurs
        if self.cleaned_data.get('trainers'):
            session.trainers.set(self.cleaned_data['trainers'])
        
        # Ajouter les dates de session
        date_count = self.cleaned_data.get('date_count', 0)
        for i in range(date_count):
            date = self.cleaned_data.get(f'date_{i}')
            room = self.cleaned_data.get(f'room_{i}')
            
            if date:
                session_date = SessionDate.objects.create(
                    session=session,
                    date=date,
                    location=room
                )
        
        return session
    

