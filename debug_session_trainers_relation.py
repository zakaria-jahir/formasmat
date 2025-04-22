import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'formation_assmat.settings')
django.setup()

from core.models import Session, Trainer

# Investigate session with ID 3
session = Session.objects.get(id=3)

# Print out the trainers directly from the database
print("Session Trainers:")
trainers = session.trainers.all()
for trainer in trainers:
    print(f"- Trainer ID: {trainer.id}, Name: {trainer.get_full_name()}")

# Check the many-to-many relationship table
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("""
        SELECT trainer_id 
        FROM core_session_trainers 
        WHERE session_id = 3
    """)
    trainer_ids = cursor.fetchall()
    print("\nTrainer IDs in many-to-many table:")
    for trainer_id in trainer_ids:
        print(f"- {trainer_id[0]}")

# Verify the relationship from the Trainer side
print("\nSessions for this trainer:")
trainer = Trainer.objects.get(id=1)  # Assuming Karine Baron is ID 1
print(f"Trainer: {trainer.get_full_name()}")
for session in trainer.sessions.all():
    print(f"- Session ID: {session.id}, Formation: {session.formation.name}")
