import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'formation_assmat.settings')
django.setup()

from core.models import Session, Trainer

# Investigate session with ID 3
session = Session.objects.get(id=3)
print(f"Session Formation: {session.formation}")
print(f"Trainers Count: {session.trainers.count()}")
print("Trainers:")
for trainer in session.trainers.all():
    print(f"- {trainer}")

# Check all trainers
print("\nAll Trainers:")
all_trainers = Trainer.objects.all()
for trainer in all_trainers:
    print(f"Trainer {trainer.id}: {trainer}")
