import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'formation_assmat.settings')

app = Celery('formation_assmat')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Configure periodic tasks
app.conf.beat_schedule = {
    'archive-old-sessions': {
        'task': 'core.tasks.archive_old_sessions',
        'schedule': crontab(hour=0, minute=0),  # Exécution quotidienne à minuit
    },
}
