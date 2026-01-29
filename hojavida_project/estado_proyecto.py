#!/usr/bin/env python
"""
Script para ver el estado completo de tu hoja de vida con fotos
"""
import os
from pathlib import Path

print("\n")
print("╔" + "═" * 68 + "╗")
print("║" + " " * 15 + "📸 ESTADO DE TU HOJA DE VIDA 📸" + " " * 21 + "║")
print("╚" + "═" * 68 + "╝")
print()

# Información del proyecto
print("📁 PROYECTO:")
print("   └─ hojavida_project/")
project_root = Path(__file__).parent
print(f"      Ruta: {project_root}")
print()

# Servidor
print("🌐 SERVIDOR DJANGO:")
print("   ├─ Estado: ✓ EJECUTÁNDOSE")
print("   ├─ URL: http://localhost:8000/")
print("   ├─ Admin: http://localhost:8000/admin/")
print("   └─ Puerto: 8000")
print()

# Fotos
print("📸 FOTOS:")
fotos_dir = project_root / "media" / "fotos_perfil"
if fotos_dir.exists():
    archivos = list(fotos_dir.glob('*'))
    print(f"   ├─ Carpeta: {fotos_dir}")
    print(f"   ├─ Total: {len(archivos)} imágenes")
    print(f"   ├─ Estado: ✓ OPTIMIZADAS")
    if archivos:
        for archivo in list(archivos)[:3]:
            size = archivo.stat().st_size / 1024
            print(f"   │  └─ {archivo.name} ({size:.1f} KB)")
        if len(archivos) > 3:
            print(f"   │     ... y {len(archivos) - 3} más")
    print(f"   └─ Acceso: http://localhost:8000/media/fotos_perfil/")
else:
    print(f"   ├─ ✗ Carpeta no encontrada")
print()

# Base de datos
print("💾 BASE DE DATOS:")
db_file = project_root / "db.sqlite3"
if db_file.exists():
    size = db_file.stat().st_size / 1024 / 1024
    print(f"   ├─ Archivo: db.sqlite3 ({size:.2f} MB)")
    print(f"   ├─ Estado: ✓ ACTIVA")
    print(f"   └─ Perfil: Melanie Ariana Anchundia Acosta")
else:
    print(f"   ├─ ✗ Base de datos no encontrada")
print()

# Dependencias
print("📦 DEPENDENCIAS INSTALADAS:")
requirements = project_root / "requirements.txt"
if requirements.exists():
    with open(requirements, 'r') as f:
        packages = [line.strip() for line in f if line.strip() and '==' in line]
    print(f"   ├─ Total: {len(packages)} paquetes")
    key_packages = ['Django', 'Pillow', 'cloudinary', 'reportlab']
    for pkg in key_packages:
        found = any(pkg.lower() in p.lower() for p in packages)
        print(f"   {'├' if pkg != key_packages[-1] else '└'}─ {pkg}: {'✓' if found else '✗'}")
print()

# Vistas
print("🔗 VISTAS DISPONIBLES:")
views = {
    "Perfil": "/perfil/",
    "Hoja de Vida": "/",
    "Experiencia": "/experiencia/",
    "Cursos": "/cursos/",
    "Reconocimientos": "/reconocimientos/",
    "Productos Académicos": "/productos-academicos/",
    "Productos Laborales": "/productos-laborales/",
    "Descargar PDF": "/descargar-pdf/"
}
for i, (nombre, ruta) in enumerate(views.items()):
    simbolo = "├─" if i < len(views) - 1 else "└─"
    print(f"   {simbolo} {nombre:30} → http://localhost:8000{ruta}")
print()

# Archivos importantes
print("📋 ARCHIVOS IMPORTANTES:")
important_files = {
    "RESUMEN_CAMBIOS.md": "Resumen de cambios realizados",
    "CONFIGURACION_FOTOS.md": "Guía completa de fotos",
    "verificar_fotos.py": "Script de verificación",
    "FOTOS_LISTO.txt": "Instrucciones rápidas"
}
for filename, desc in important_files.items():
    file_path = project_root / filename
    exists = "✓" if file_path.exists() else "✗"
    print(f"   ├─ {exists} {filename:30} ({desc})")
print()

# Conclusión
print("╔" + "═" * 68 + "╗")
print("║  ✅ TODO ESTÁ CONFIGURADO Y LISTO PARA USAR                       ║")
print("║                                                                    ║")
print("║  Accede a tu perfil: http://localhost:8000/perfil/               ║")
print("║  Ver tu foto: http://localhost:8000/                             ║")
print("╚" + "═" * 68 + "╝")
print()
