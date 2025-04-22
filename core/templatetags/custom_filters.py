from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='divide_by')
def divide_by(value, arg):
    """Divise une valeur par un argument"""
    try:
        return float(value) / float(arg) if float(arg) != 0 else 0
    except (ValueError, TypeError):
        return 0

@register.filter(name='multiply')
def multiply(value, arg):
    """Multiplie une valeur par un argument"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0
