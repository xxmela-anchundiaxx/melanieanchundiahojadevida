Despliegue a Render (resumen rápido)

1. Crear un repo git y subir tu proyecto.
2. En Render: New -> Web Service -> Conectar tu repo.
   - Build Command: pip install -r requirements.txt && python manage.py collectstatic --noinput
   - Start Command: gunicorn hojavida_project.wsgi:application --bind 0.0.0.0:$PORT
3. Configurar Environment Variables en el servicio Web en Render:
   - SECRET_KEY (requerido)
   - DEBUG=False
   - DATABASE_URL (puedes crear un Postgres DB en Render)
   - CLOUDINARY_URL (opcional: si la pones, el proyecto usará Cloudinary para media)
   - ALLOWED_HOSTS (ej. my-app.onrender.com)
4. Añadir servicio Postgres en Render (Databases -> New Database). Copia DATABASE_URL al Web Service.
5. Hacer deploy. Después, ejecutar en la consola de Render:
   python manage.py migrate
   python manage.py createsuperuser
6. Verificar:
   - Archivos estáticos sirven correctamente
   - Archivos de media si usas Cloudinary se sirven desde Cloudinary

Notas:
- No subas la carpeta `media/` al repositorio (Render es efímero).
- Si no quieres usar Cloudinary, puedes mantener almacenamiento local solo en desarrollo.
