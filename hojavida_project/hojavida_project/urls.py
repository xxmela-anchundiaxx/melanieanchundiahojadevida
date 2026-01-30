"""
URL configuration for hojavida_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLConf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import temporal para endpoint de administración segura (migraciones remotas)
from curriculum import views_admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('curriculum.urls')),
    # Endpoint TEMPORAL y protegido para ejecutar migraciones sin acceso a la shell.
    # Requiere el header `X-MIGRATE-SECRET` con el valor de la variable de entorno MIGRATE_SECRET.
    path('__run_migrations__/', views_admin.run_migrations_endpoint, name='run_migrations_endpoint'),
]

# Servir archivos multimedia en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)