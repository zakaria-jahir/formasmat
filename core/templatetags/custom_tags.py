# core/templatetags/custom_tags.py

from django import template
from core.utils import haversine1 as haversine  # ou haversine si tu l'as renommée

register = template.Library()

@register.filter
def get_distance(session, user):
    if (
        session.latitude is not None and session.longitude is not None and
        user.latitude is not None and user.longitude is not None
    ):
        return round(haversine(user.latitude, user.longitude, session.latitude, session.longitude), 1)
    return "?"
