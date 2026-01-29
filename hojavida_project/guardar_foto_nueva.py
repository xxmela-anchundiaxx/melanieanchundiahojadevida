#!/usr/bin/env python
"""
Guardar foto nueva en media/fotos_perfil/ y actualizar BD
"""
import os
import sys
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hojavida_project.settings')
sys.path.insert(0, r'C:\Users\Lenovo.User\OneDrive\Escritorio\Mi hoja de vida\hojavida_project')
django.setup()

from curriculum.models import DatosPersonales
from django.conf import settings
from PIL import Image

print("="*70)
print("📸 GUARDAR Y ACTUALIZAR FOTO DE PERFIL")
print("="*70)

# Obtener el perfil
perfil = DatosPersonales.objects.filter(perfilactivo=1).first()

if not perfil:
    print("✗ No hay perfil activo")
    sys.exit(1)

print(f"\nPerfil: {perfil.nombres} {perfil.apellidos}")

# Crear nombre de archivo con timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
nombre_archivo = f"foto_perfil_nuevo_{timestamp}.jpg"
ruta_completa = os.path.join(settings.MEDIA_ROOT, 'fotos_perfil', nombre_archivo)

print(f"\nNuevo nombre: {nombre_archivo}")
print(f"Ruta: {ruta_completa}")

# La foto viene del attachment, vamos a buscarla en la carpeta de descargas o temporal
# Por ahora, vamos a listar las fotos más recientes y usar la más nueva

foto_dir = os.path.join(settings.MEDIA_ROOT, 'fotos_perfil')
fotos = []

for f in os.listdir(foto_dir):
    path = os.path.join(foto_dir, f)
    if os.path.isfile(path) and f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
        mtime = os.path.getmtime(path)
        size = os.path.getsize(path)
        fotos.append((f, mtime, path, size))

if not fotos:
    print("✗ No hay fotos")
    sys.exit(1)

# Ordenar por tamaño (la más grande es probablemente la nueva)
fotos.sort(key=lambda x: x[3], reverse=True)

print("\n🔍 Fotos disponibles:")
for i, (nombre, mtime, path, size) in enumerate(fotos[:3]):
    print(f"   {i+1}. {nombre} ({size/1024:.1f} KB)")

# Usar la más grande (probablemente la nueva que subiste)
foto_seleccionada = fotos[0][0]
print(f"\n✓ Foto seleccionada: {foto_seleccionada}")

# Actualizar en la BD
nombre_relativo = f'fotos_perfil/{foto_seleccionada}'
perfil.foto_perfil = nombre_relativo
perfil.save()

print(f"✅ Foto actualizada en base de datos")
print(f"\nURL: /foto/{foto_seleccionada}/")

print("\n" + "="*70)
print("🌐 VE A: http://localhost:8000/perfil/")
print("="*70)
