#!/usr/bin/env python
"""
Prueba la ruta /foto/<filename>/
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hojavida_project.settings')
sys.path.insert(0, r'C:\Users\Lenovo.User\OneDrive\Escritorio\Mi hoja de vida\hojavida_project')
django.setup()

from django.test import Client
from curriculum.models import DatosPersonales

print("="*70)
print("🧪 PRUEBA DE LA VISTA SERVIR_FOTO")
print("="*70)

# Obtener perfil y foto
perfil = DatosPersonales.objects.filter(perfilactivo=1).first()
if not perfil or not perfil.foto_perfil:
    print("✗ No hay perfil o foto")
    sys.exit(1)

filename = os.path.basename(perfil.foto_perfil.name)
print(f"\nFoto: {filename}")

# Crear cliente de prueba
client = Client()

# Probar la URL
url = f'/foto/{filename}/'
print(f"URL a probar: {url}")

try:
    response = client.get(url)
    print(f"\nEstatus: {response.status_code}")
    print(f"Content-Type: {response.get('Content-Type', 'No especificado')}")
    print(f"Tamaño: {len(response.content)} bytes")
    
    if response.status_code == 200:
        print("\n✅ ¡LA FOTO SE SIRVE CORRECTAMENTE!")
    else:
        print("\n✗ Error en la respuesta")
        print(f"Contenido: {response.content[:200]}")
except Exception as e:
    print(f"\n✗ Error: {e}")

print("\n" + "="*70)
