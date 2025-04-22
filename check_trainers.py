import os
import django

# Configurer le chemin du projet Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'formation_assmat.settings')
django.setup()

from core.models import Trainer

# Récupérer tous les formateurs
trainers = Trainer.objects.all()

print("Nombre de formateurs :", trainers.count())
for trainer in trainers:
    print(f"ID: {trainer.id}, Nom: {trainer.first_name} {trainer.last_name}, Email: {trainer.email}")
