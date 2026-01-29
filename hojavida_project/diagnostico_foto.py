#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hojavida_project.settings')
sys.path.insert(0, r'C:\Users\Lenovo.User\OneDrive\Escritorio\Mi hoja de vida\hojavida_project')
django.setup()

from curriculum.models import DatosPersonales
from django.conf import settings
from django.test import Client

print("="*70)
print("🔍 DIAGNÓSTICO: ¿POR QUÉ NO CARGA LA FOTO?")
print("="*70)

# 1. Verificar BD
perfil = DatosPersonales.objects.filter(perfilactivo=1).first()
if not perfil:
    print("\n✗ No hay perfil activo")
    sys.exit(1)

print(f"\n1️⃣ PERFIL:")
print(f"   Nombre: {perfil.nombres} {perfil.apellidos}")

if perfil.foto_perfil and perfil.foto_perfil.name:
    print(f"   Foto en BD: {perfil.foto_perfil.name}")
    print(f"   URL en BD: {perfil.foto_perfil.url}")
else:
    print(f"   ✗ Sin foto en BD")

# 2. Verificar archivo
if perfil.foto_perfil:
    path = perfil.foto_perfil.path
    print(f"\n2️⃣ ARCHIVO:")
    print(f"   Path: {path}")
    existe = os.path.exists(path)
    print(f"   Existe: {'✓' if existe else '✗'}")
    if existe:
        size = os.path.getsize(path)
        print(f"   Tamaño: {size} bytes")

# 3. Verificar vista servir_foto
print(f"\n3️⃣ VISTA servir_foto:")
if perfil.foto_perfil:
    filename = os.path.basename(perfil.foto_perfil.name)
    url = f'/foto/{filename}/'
    print(f"   URL esperada: {url}")
    
    client = Client()
    response = client.get(url)
    print(f"   Estatus: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✓ Vista funciona correctamente")
    else:
        print(f"   ✗ Error en la vista: {response.status_code}")

# 4. Verificar template
print(f"\n4️⃣ TEMPLATE (perfil.html):")
print(f"   Debe generar: <img src=\"/foto/{filename}/\" ...>")

print("\n" + "="*70)
