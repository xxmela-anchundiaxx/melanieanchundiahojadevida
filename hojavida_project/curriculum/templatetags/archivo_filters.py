import os
from django import template

register = template.Library()

@register.filter
def basename(value):
    """Extrae solo el nombre del archivo de una ruta"""
    if value:
        return os.path.basename(str(value))
    return value
