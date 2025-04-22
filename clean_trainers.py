import os
import django

# Configurer le chemin du projet Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'formation_assmat.settings')
django.setup()

from core.models import Trainer

# Supprimer les formateurs vides
empty_trainers = Trainer.objects.filter(first_name__isnull=True, last_name__isnull=True)
print("Nombre de formateurs vides :", empty_trainers.count())
empty_trainers.delete()

# Afficher les formateurs restants
trainers = Trainer.objects.all()
print("\nFormateurs restants :")
for trainer in trainers:
    print(f"ID: {trainer.id}, Nom: {trainer.first_name} {trainer.last_name}, Email: {trainer.email}")
