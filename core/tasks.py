from celery import shared_task
from django.utils import timezone
from .models import Session
import logging

logger = logging.getLogger(__name__)

@shared_task
def archive_old_sessions():
    """Tâche périodique pour archiver les anciennes sessions."""
    try:
        count = Session.archive_old_sessions()
        logger.info(f"{count} sessions ont été archivées")
        return count
    except Exception as e:
        logger.error(f"Erreur lors de l'archivage des sessions : {str(e)}")
        raise
