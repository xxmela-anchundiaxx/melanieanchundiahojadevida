#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hojavida_project.settings')
sys.path.insert(0, '/Users/Lenovo.User/OneDrive/Escritorio/Mi hoja de vida/hojavida_project')
django.setup()

from django.conf import settings
from curriculum.models import DatosPersonales

print("="*70)
print("🔍 DIAGNÓSTICO COMPLETO DE FOTOS")
print("="*70)

# Verificar configuración
print("\n1️⃣ CONFIGURACIÓN DJANGO:")
print(f"   DEBUG: {settings.DEBUG}")
print(f"   MEDIA_URL: {settings.MEDIA_URL}")
print(f"   MEDIA_ROOT: {settings.MEDIA_ROOT}")

# Verificar carpeta
print("\n2️⃣ SISTEMA DE ARCHIVOS:")
media_root = settings.MEDIA_ROOT
print(f"   MEDIA_ROOT existe: {os.path.exists(media_root)}")

foto_dir = os.path.join(media_root, 'fotos_perfil')
print(f"   fotos_perfil existe: {os.path.exists(foto_dir)}")

if os.path.exists(foto_dir):
    files = os.listdir(foto_dir)
    print(f"   Total archivos: {len(files)}")
    for f in files[:5]:
        path = os.path.join(foto_dir, f)
        size = os.path.getsize(path) / 1024
        print(f"      ✓ {f} ({size:.1f} KB)")

# Verificar BD
print("\n3️⃣ BASE DE DATOS:")
perfil = DatosPersonales.objects.filter(perfilactivo=1).first()
if perfil:
    print(f"   Perfil: {perfil.nombres} {perfil.apellidos}")
    if perfil.foto_perfil:
        print(f"   Foto nombre: {perfil.foto_perfil.name}")
        print(f"   Foto URL: {perfil.foto_perfil.url}")
        path = perfil.foto_perfil.path
        print(f"   Foto path: {path}")
        existe = os.path.exists(path)
        print(f"   Archivo existe: {'✓' if existe else '✗'} {existe}")
        if existe:
            size = os.path.getsize(path) / 1024
            print(f"   Tamaño: {size:.1f} KB")
    else:
        print(f"   ✗ Sin foto asignada")
else:
    print(f"   ✗ No hay perfil activo")

# Verificar acceso a archivos
print("\n4️⃣ PRUEBA DE ACCESO:")
if perfil and perfil.foto_perfil:
    path = perfil.foto_perfil.path
    try:
        with open(path, 'rb') as f:
            data = f.read()
            print(f"   ✓ Archivo accesible (lectura OK)")
            print(f"   ✓ Bytes leídos: {len(data)}")
    except Exception as e:
        print(f"   ✗ Error al leer: {e}")

print("\n" + "="*70)
