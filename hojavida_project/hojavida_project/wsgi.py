"""
WSGI config for hojavida_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Determine correct settings module regardless of how the package is imported (Render may prefix the root)
if os.environ.get('DJANGO_SETTINGS_MODULE') is None:
    try:
        # prefer the standard import (works when working dir is the inner package)
        import importlib
        importlib.import_module('hojavida_project.settings')
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hojavida_project.settings')
    except Exception:
        # fallback when Render/Start command causes a doubled package path
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hojavida_project.hojavida_project.settings')

application = get_wsgi_application()
