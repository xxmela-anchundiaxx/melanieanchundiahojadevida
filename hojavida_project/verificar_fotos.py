#!/usr/bin/env python
"""
Script para verificar que las fotos se están sirviendo correctamente
"""
import os
import sys
from pathlib import Path

# Agregar proyecto al path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hojavida_project.settings')

import django
django.setup()

from django.conf import settings
from curriculum.models import DatosPersonales

print("\n" + "="*60)
print("🔍 VERIFICACIÓN DE FOTOS DE PERFIL")
print("="*60 + "\n")

# Verificar configuración
print("📋 CONFIGURACIÓN DE DJANGO:")
print(f"   MEDIA_ROOT: {settings.MEDIA_ROOT}")
print(f"   MEDIA_URL: {settings.MEDIA_URL}")
print(f"   DEBUG: {settings.DEBUG}")
print()

# Verificar carpeta
media_root = settings.MEDIA_ROOT
fotos_dir = media_root / 'fotos_perfil'
print(f"📂 CARPETAS:")
print(f"   Media existe: {'✓' if media_root.exists() else '✗'} {media_root}")
print(f"   Fotos existe: {'✓' if fotos_dir.exists() else '✗'} {fotos_dir}")

if fotos_dir.exists():
    archivos = list(fotos_dir.glob('*'))
    print(f"   Archivos: {len(archivos)}")
    for archivo in archivos[:5]:
        print(f"      - {archivo.name} ({archivo.stat().st_size / 1024:.1f} KB)")
    if len(archivos) > 5:
        print(f"      ... y {len(archivos) - 5} más")
print()

# Verificar base de datos
print("💾 BASE DE DATOS:")
perfiles = DatosPersonales.objects.filter(perfilactivo=1)
print(f"   Perfiles activos: {perfiles.count()}")

for perfil in perfiles:
    print(f"\n   👤 {perfil.nombres} {perfil.apellidos}")
    if perfil.foto_perfil:
        print(f"      ✓ Foto: {perfil.foto_perfil.name}")
        print(f"      ✓ URL: {perfil.foto_perfil.url}")
        ruta_real = perfil.foto_perfil.path
        existe = os.path.exists(ruta_real)
        print(f"      {'✓' if existe else '✗'} Archivo existe: {ruta_real}")
        if existe:
            tamaño = os.path.getsize(ruta_real) / 1024
            print(f"      📊 Tamaño: {tamaño:.1f} KB")
    else:
        print(f"      ✗ Sin foto asignada")

print("\n" + "="*60)
print("✅ VERIFICACIÓN COMPLETADA")
print("="*60)
print("\n🌐 Accede a:")
print(f"   Perfil: http://localhost:8000/perfil/")
print(f"   Admin: http://localhost:8000/admin/")
print()
