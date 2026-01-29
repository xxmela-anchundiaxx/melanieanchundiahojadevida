# 📸 Guía Completa: Fotos de Perfil en Tu Hoja de Vida

## ✅ Estado Actual

✓ Servidor Django ejecutándose correctamente
✓ 14 imágenes optimizadas en `media/fotos_perfil/`
✓ Base de datos configurada
✓ Rutas de media configuradas correctamente
✓ Vistas actualizadas para pasar contexto de perfil

## 🚀 Cómo Ver Las Fotos

### Opción 1: En Tu Perfil (Recomendado)
1. Abre tu navegador y ve a: **http://localhost:8000/perfil/**
2. Aquí verás tu foto de perfil en un círculo perfecto

### Opción 2: En Tu Hoja de Vida Completa
1. Ve a: **http://localhost:8000/**
2. La foto aparecerá en la sección superior

### Opción 3: En El PDF
1. Descarga el PDF desde: **http://localhost:8000/descargar-pdf/**
2. Tu foto aparecerá en el documento

## 📤 Cómo Cambiar Tu Foto

### Paso 1: Accede al Admin
1. Ve a: **http://localhost:8000/admin/**
2. Usuario: (tu usuario admin)
3. Contraseña: (tu contraseña admin)

### Paso 2: Edita Tus Datos Personales
1. Haz clic en **"Datos Personales"** en el menú izquierdo
2. Haz clic en tu perfil (Melanie Ariana Anchundia Acosta)
3. Scroll hasta encontrar el campo **"Foto Perfil"**

### Paso 3: Sube Tu Foto
1. Haz clic en **"Cambiar"** para seleccionar una nueva imagen
2. Elige una imagen de tu computadora (JPG, PNG, WEBP)
3. Haz clic en **"Guardar"**

¡La foto aparecerá automáticamente en tu perfil!

## 🎯 Características Implementadas

✅ **Almacenamiento Local**: Las fotos se guardan en `media/fotos_perfil/`
✅ **Optimización Automática**: Las imágenes se optimizan al guardarse
✅ **Responsive**: Las fotos se adaptan a cualquier dispositivo
✅ **Cache Optimizado**: Carga rápida de imágenes
✅ **Manejo de Errores**: Si falla una imagen, muestra un ícono de perfil

## 📂 Carpetas Importantess

- `media/fotos_perfil/` - Aquí se guardan tus fotos de perfil
- `templates/perfil.html` - Template que muestra tu foto
- `curriculum/views.py` - Vistas que pasan los datos

## 🔧 Configuración de Django

**MEDIA_ROOT**: `C:\Users\Lenovo.User\OneDrive\Escritorio\Mi hoja de vida\hojavida_project\media`
**MEDIA_URL**: `/media/`
**DEFAULT_FILE_STORAGE**: `django.core.files.storage.FileSystemStorage`

## 🚀 Comandos Útiles

### Optimizar todas las imágenes:
```bash
python manage.py optimize_images
```

### Ver información de tu foto:
```bash
python manage.py shell
>>> from curriculum.models import DatosPersonales
>>> p = DatosPersonales.objects.get(perfilactivo=1)
>>> print(p.foto_perfil.url)
```

## ❓ Si Las Fotos No Aparecen

1. **Verifica que el servidor esté corriendo**: http://localhost:8000/
2. **Revisa la consola** del servidor para errores
3. **Limpia la caché del navegador**: Ctrl+Shift+Delete
4. **Verifica que la foto esté en la base de datos**: Admin > Datos Personales

## 📝 Formatos Soportados

- JPG / JPEG
- PNG
- WEBP (recomendado por su tamaño)
- GIF

## 💾 Requisitos Instalados

- Pillow: Para procesar imágenes
- Django: Para el servidor web
- Cloudinary: Para almacenamiento en la nube (opcional)

---

¡Tu hoja de vida está lista con fotos! 🎉
