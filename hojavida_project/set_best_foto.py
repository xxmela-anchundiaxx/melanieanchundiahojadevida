#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hojavida_project.settings')
sys.path.insert(0, r'C:\Users\Lenovo.User\OneDrive\Escritorio\Mi hoja de vida\hojavida_project')
django.setup()

from curriculum.models import DatosPersonales

# Obtener perfil y actualizar
perfil = DatosPersonales.objects.filter(perfilactivo=1).first()

if perfil:
    # Usar la foto más hermosa que compartiste
    perfil.foto_perfil = 'fotos_perfil/foto_formal_1lTidOq.jpg'
    perfil.save()
    print("✅ Foto actualizada!")
    print(f"   Nueva foto: fotos_perfil/foto_formal_1lTidOq.jpg")
    print(f"   URL: /foto/foto_formal_1lTidOq.jpg/")
else:
    print("✗ No hay perfil")
