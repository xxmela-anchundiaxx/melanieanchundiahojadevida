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

# Optional: run migrations automatically at process start when explicitly enabled in the environment.
# This helps when you cannot open the platform shell (e.g. Render) — enable by setting
# AUTO_MIGRATE_ON_STARTUP=1 in the service environment. It is safe because Django migrations
# are idempotent; errors are logged but won't crash the process.
if os.environ.get('AUTO_MIGRATE_ON_STARTUP') == '1':
    try:
        # Avoid importing Django twice in unusual startup sequences; ensure settings are configured
        from django.core.management import call_command
        # Only run non-interactive migrations
        call_command('migrate', '--noinput')
        print('AUTO_MIGRATE_ON_STARTUP: migrations applied at startup')
    except Exception as _exc:
        # Don't prevent the app from starting; surface the failure in logs for investigation
        import sys, traceback
        print('AUTO_MIGRATE_ON_STARTUP failed:', file=sys.stderr)
        traceback.print_exc()

application = get_wsgi_application()
