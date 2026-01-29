from django.urls import path
from .views import (
    hoja_vida,
    descargar_pdf,
    perfil,
    experiencia,
    cursos,
    productos_academicos,
    productos_laborales,
    reconocimientos,
    venta_garage,
    servir_foto,
    servir_imagen,
)

urlpatterns = [
    path('', hoja_vida, name='hoja_vida'),
    path('descargar-pdf/', descargar_pdf, name='descargar_pdf'),
    path('perfil/', perfil, name='perfil'),
    path('experiencia/', experiencia, name='experiencia'),
    path('cursos/', cursos, name='cursos'),
    path('productos-academicos/', productos_academicos, name='productos_academicos'),
    path('productos-laborales/', productos_laborales, name='productos_laborales'),
    path('reconocimientos/', reconocimientos, name='reconocimientos'),
    path('venta-garage/', venta_garage, name='venta_garage'),
    path('foto/<str:filename>/', servir_foto, name='servir_foto'),
    path('imagen/<path:carpeta>/<str:filename>/', servir_imagen, name='servir_imagen'),
]
