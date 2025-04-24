from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import TrainingRoom
from .utils import get_coordinates_from_address

@receiver(pre_save, sender=TrainingRoom)
def fill_coordinates(sender, instance, **kwargs):
    if (not instance.latitude or not instance.longitude) and instance.address:
        lat, lon = get_coordinates_from_address(
            instance.address,
            postal_code=instance.postal_code,
            city=instance.city
        )
        instance.latitude = lat
        instance.longitude = lon
