#!/usr/bin/env python
"""
Guardar foto nueva en carpeta y actualizar base de datos
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
import base64

print("="*70)
print("📸 ACTUALIZAR FOTO DE PERFIL")
print("="*70)

# Obtener el perfil
perfil = DatosPersonales.objects.filter(perfilactivo=1).first()

if not perfil:
    print("✗ No hay perfil activo")
    sys.exit(1)

print(f"\nPerfil: {perfil.nombres} {perfil.apellidos}")

# Buscar la foto más reciente (que es la que el usuario acaba de subir)
foto_dir = os.path.join(settings.MEDIA_ROOT, 'fotos_perfil')

if not os.path.exists(foto_dir):
    os.makedirs(foto_dir, exist_ok=True)
    print("✗ Carpeta creada pero sin fotos")
    sys.exit(1)

# Listar fotos ordenadas por tamaño (la más grande es la nueva que subió)
fotos = []
for f in os.listdir(foto_dir):
    path = os.path.join(foto_dir, f)
    if os.path.isfile(path) and f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif')):
        size = os.path.getsize(path)
        mtime = os.path.getmtime(path)
        fotos.append({'nombre': f, 'path': path, 'size': size, 'mtime': mtime})

if not fotos:
    print("✗ No hay fotos en media/fotos_perfil/")
    sys.exit(1)

# Mostrar las fotos
print(f"\n📁 Fotos encontradas ({len(fotos)}):")
for i, foto in enumerate(fotos[:5]):
    print(f"   {i+1}. {foto['nombre']:<40} ({foto['size']/1024:>6.1f} KB)")

# Buscar una foto que tenga característica de ser "nueva" (más grande, por ejemplo)
# Ordenar por tamaño descendente y tomar las grandes (más de 100KB probablemente es foto nueva)
fotos_grandes = [f for f in fotos if f['size'] > 80000]  # Más de 80KB

if fotos_grandes:
    fotos_grandes.sort(key=lambda x: x['size'], reverse=True)
    foto_nueva = fotos_grandes[0]
else:
    # Si no hay fotos grandes, tomar la más reciente
    fotos.sort(key=lambda x: x['mtime'], reverse=True)
    foto_nueva = fotos[0]

print(f"\n✓ Foto seleccionada: {foto_nueva['nombre']}")
print(f"  Tamaño: {foto_nueva['size']/1024:.1f} KB")

# Actualizar en BD
nombre_relativo = f"fotos_perfil/{foto_nueva['nombre']}"
perfil.foto_perfil = nombre_relativo
perfil.save()

print(f"\n✅ FOTO ACTUALIZADA EN BASE DE DATOS!")
print(f"   Ruta: {nombre_relativo}")
print(f"   URL: /foto/{foto_nueva['nombre']}/")

print("\n" + "="*70)
print("🌐 Tu foto ahora está en:")
print("   http://localhost:8000/perfil/")
print("   http://localhost:8000/")
print("="*70)
