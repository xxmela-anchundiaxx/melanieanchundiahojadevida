import os
import io
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.management import call_command

# Endpoint para ejecutar migraciones en producción cuando no hay acceso al shell.
# Seguridad:
# - Requiere header `X-MIGRATE-SECRET` que debe coincidir con la variable de entorno MIGRATE_SECRET
# - Después de ejecutar con éxito crea un marcador en /tmp para evitar ejecuciones repetidas
# - Diseñado para ser temporal: eliminar después de usar

MIGRATE_MARKER = '/tmp/.migrations_ran'

@csrf_exempt
@require_POST
def run_migrations_endpoint(request):
    secret_env = os.environ.get('MIGRATE_SECRET')
    provided = request.headers.get('X-MIGRATE-SECRET') or request.POST.get('secret')

    if not secret_env:
        return JsonResponse({'error': 'MIGRATE_SECRET not configured on server'}, status=403)
    if not provided or provided != secret_env:
        return JsonResponse({'error': 'invalid secret'}, status=401)

    if os.path.exists(MIGRATE_MARKER):
        return JsonResponse({'status': 'already_ran'}, status=200)

    # Ejecutar migrate y capturar la salida
    out = io.StringIO()
    err = io.StringIO()
    try:
        call_command('migrate', '--noinput', stdout=out, stderr=err)
        # marcar como ejecutado
        try:
            with open(MIGRATE_MARKER, 'w') as f:
                f.write('ok')
        except Exception:
            # no crítico
            pass
        return JsonResponse({'status': 'ok', 'stdout': out.getvalue(), 'stderr': err.getvalue()})
    except Exception as exc:
        return JsonResponse({'status': 'error', 'exc': str(exc), 'stdout': out.getvalue(), 'stderr': err.getvalue()}, status=500)
