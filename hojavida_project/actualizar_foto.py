#!/usr/bin/env python
"""
Script para actualizar la foto de perfil con la nueva foto
"""
import os
import sys
import django
from PIL import Image
from io import BytesIO

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hojavida_project.settings')
sys.path.insert(0, r'C:\Users\Lenovo.User\OneDrive\Escritorio\Mi hoja de vida\hojavida_project')
django.setup()

from django.core.files.base import ContentFile
from curriculum.models import DatosPersonales
from django.conf import settings

print("="*70)
print("📸 ACTUALIZAR FOTO DE PERFIL")
print("="*70)

# Obtener el perfil
perfil = DatosPersonales.objects.filter(perfilactivo=1).first()

if not perfil:
    print("✗ No hay perfil activo")
    sys.exit(1)

print(f"\nPerfil: {perfil.nombres} {perfil.apellidos}")

# Buscar la foto más nueva que sea selfie (la que el usuario subió)
# Vamos a usar la foto en la attachment que aparentemente es foto_formal_1lTidOq.jpg o similar
# Buscar la foto más reciente

foto_dir = os.path.join(settings.MEDIA_ROOT, 'fotos_perfil')
if not os.path.exists(foto_dir):
    print("✗ Carpeta fotos_perfil no existe")
    sys.exit(1)

# Obtener lista de fotos ordenadas por fecha de modificación (más reciente primero)
fotos = []
for f in os.listdir(foto_dir):
    path = os.path.join(foto_dir, f)
    if os.path.isfile(path) and f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif')):
        mtime = os.path.getmtime(path)
        fotos.append((f, mtime, path))

if not fotos:
    print("✗ No hay fotos en la carpeta")
    sys.exit(1)

# Ordenar por fecha más reciente
fotos.sort(key=lambda x: x[1], reverse=True)

# Usar la más reciente
foto_actual = fotos[0][0]
print(f"\nFoto más reciente encontrada: {foto_actual}")
print(f"Fecha: {fotos[0][1]}")

# Actualizar el modelo
nombre_foto = f'fotos_perfil/{foto_actual}'
perfil.foto_perfil = nombre_foto
perfil.save()

print(f"\n✅ Foto actualizada correctamente!")
print(f"\nDetalles:")
print(f"  Nombre archivo: {foto_actual}")
print(f"  Ruta en BD: {nombre_foto}")
print(f"  URL de servicio: /foto/{foto_actual}/")

print("\n" + "="*70)
print("🌐 Tu foto ahora está visible en:")
print("   http://localhost:8000/perfil/")
print("="*70)
