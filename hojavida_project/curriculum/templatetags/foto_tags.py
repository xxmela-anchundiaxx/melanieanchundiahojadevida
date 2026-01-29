from django import template
import os

register = template.Library()

@register.filter
def foto_url(foto_obj):
    """Retorna la URL correcta para servir una foto"""
    if not foto_obj or not foto_obj.name:
        return ''
    
    # Extraer solo el nombre del archivo
    filename = os.path.basename(foto_obj.name)
    
    # Retornar la URL a través de la vista servir_foto
    return f'/foto/{filename}/'
