# 🔧 CORRECCIÓN: Foto de Perfil en Django

## ¿Cuál era el problema?

El template `perfil.html` usaba:
```django
{% with filename=perfil.foto_perfil.name|slice:"-50:" %}
```

Esto extraía **los últimos 50 caracteres** de `"fotos_perfil/foto_formal_1lTidOq.jpg"`, lo que resultaba en:
- `fotos_perfil/foto_formal_1lTidOq.jpg` (la ruta completa)

Pero la vista `servir_foto()` esperaba:
- Solo `foto_formal_1lTidOq.jpg` (solo el nombre)

Por eso la URL se generaba como:
```
❌ /foto/fotos_perfil/foto_formal_1lTidOq.jpg/  (INCORRECTO)
```

## ¿Cómo se arregló?

### 1. Creé un filtro custom `basename` 📦

Archivo: `curriculum/templatetags/archivo_filters.py`

```python
import os
from django import template

register = template.Library()

@register.filter
def basename(value):
    """Extrae solo el nombre del archivo de una ruta"""
    if value:
        return os.path.basename(str(value))
    return value
```

### 2. Actualicé el template `perfil.html` ✏️

Cambié de:
```django
{% with filename=perfil.foto_perfil.name|slice:"-50:" %}
```

A:
```django
{% load archivo_filters %}
{% with filename=perfil.foto_perfil.name|basename %}
```

Ahora la URL se genera correctamente:
```
✅ /foto/foto_formal_1lTidOq.jpg/  (CORRECTO)
```

## ¿Qué hacer ahora?

1. **Reinicia el servidor Django:**
   ```
   python manage.py runserver
   ```

2. **Recarga la página del navegador:**
   - http://localhost:8000/perfil

3. **Verifica que la foto aparezca** en el círculo (antes solo estaba el círculo vacío)

## Archivos modificados

- ✏️ [templates/perfil.html](templates/perfil.html) - Agregó `{% load archivo_filters %}` y cambió el filtro
- ✏️ [curriculum/templatetags/archivo_filters.py](curriculum/templatetags/archivo_filters.py) - Filtro custom nuevo

## Verificación

Si quieres verificar que todo está correcto, ejecuta:
```
python verificar_foto.py
```

Este script confirmará que:
- La foto existe en el servidor de archivos
- La vista `servir_foto()` devuelve la imagen (status 200)
- El tamaño del archivo es correcto
