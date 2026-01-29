#!/usr/bin/env python
"""
Script para verificar que la foto carga correctamente desde el navegador
"""
import os
import sys

# Agregar proyecto al path
sys.path.insert(0, r'C:\Users\Lenovo.User\OneDrive\Escritorio\Mi hoja de vida\hojavida_project')

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hojavida_project.settings')

import django
django.setup()

from django.test import Client
from curriculum.models import DatosPersonales
import os.path

print("="*70)
print("✅ VERIFICANDO CARGA DE FOTO")
print("="*70)

# 1. Obtener perfil activo
perfil = DatosPersonales.objects.filter(perfilactivo=1).first()
if not perfil:
    print("❌ No hay perfil activo")
    sys.exit(1)

print(f"\n📋 Perfil: {perfil.nombres} {perfil.apellidos}")

# 2. Verificar foto en BD
if not perfil.foto_perfil or not perfil.foto_perfil.name:
    print("❌ Sin foto en la BD")
    sys.exit(1)

print(f"📸 Foto en BD: {perfil.foto_perfil.name}")

# 3. Extraer solo nombre del archivo
filename = os.path.basename(perfil.foto_perfil.name)
print(f"📄 Nombre del archivo: {filename}")

# 4. Verificar que el archivo existe
file_path = perfil.foto_perfil.path
if not os.path.exists(file_path):
    print(f"❌ Archivo no existe: {file_path}")
    sys.exit(1)

size = os.path.getsize(file_path)
print(f"✓ Archivo existe: {size} bytes")

# 5. Probar la vista servir_foto
print(f"\n🌐 Probando la vista...")
client = Client()
url = f'/foto/{filename}/'
print(f"   URL: {url}")

response = client.get(url)
print(f"   Status: {response.status_code}")

if response.status_code == 200:
    print(f"   ✅ LA VISTA FUNCIONA CORRECTAMENTE")
    print(f"   Content-Type: {response.get('Content-Type')}")
    print(f"   Tamaño respuesta: {len(response.content)} bytes")
else:
    print(f"   ❌ ERROR: {response.status_code}")
    if response.status_code == 404:
        print(f"   El archivo no se encontró")
    print(f"   Contenido: {response.content[:200]}")

print("\n" + "="*70)
print("✅ PRÓXIMOS PASOS:")
print("   1. Reinicia el servidor Django: python manage.py runserver")
print("   2. Abre http://localhost:8000/perfil en tu navegador")
print("   3. La foto debe aparecer en el círculo")
print("="*70)
