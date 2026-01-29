from django.core.management.base import BaseCommand
from django.conf import settings
from PIL import Image
import os

class Command(BaseCommand):
    help = 'Optimiza las imágenes de fotos de perfil'

    def handle(self, *args, **options):
        media_root = settings.MEDIA_ROOT
        fotos_dir = os.path.join(media_root, 'fotos_perfil')
        
        if not os.path.exists(fotos_dir):
            self.stdout.write(self.style.WARNING('La carpeta fotos_perfil no existe'))
            return

        optimized_count = 0
        for filename in os.listdir(fotos_dir):
            filepath = os.path.join(fotos_dir, filename)
            
            if os.path.isfile(filepath) and filename.lower().endswith(('jpg', 'jpeg', 'png', 'gif', 'webp')):
                try:
                    img = Image.open(filepath)
                    
                    # Convertir a RGB si es necesario
                    if img.mode in ('RGBA', 'LA', 'P'):
                        rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                        rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                        img = rgb_img
                    
                    # Redimensionar si es muy grande
                    max_width = 2000
                    max_height = 2000
                    if img.width > max_width or img.height > max_height:
                        img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                    
                    # Guardar optimizado
                    img.save(filepath, quality=85, optimize=True)
                    optimized_count += 1
                    self.stdout.write(self.style.SUCCESS(f'✓ Optimizada: {filename}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'✗ Error en {filename}: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS(f'\nTotal optimizadas: {optimized_count} imágenes'))
