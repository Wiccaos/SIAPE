from django.conf import settings

from .models import Notificacion


def static_asset_version(request):
    return {'STATIC_CACHE_BUST': getattr(settings, 'STATIC_CACHE_BUST', '1')}


def notificaciones_usuario(request):
    if not request.user.is_authenticated:
        return {'notificaciones_header': [], 'notificaciones_no_leidas_count': 0}

    try:
        rol_nombre = request.user.perfil.rol.nombre_rol
    except AttributeError:
        return {'notificaciones_header': [], 'notificaciones_no_leidas_count': 0}

    qs = Notificacion.objects.filter(rol_destino=rol_nombre).select_related('solicitud')
    notificaciones_header = list(qs[:12])
    no_leidas = qs.filter(leida=False).count()

    return {
        'notificaciones_header': notificaciones_header,
        'notificaciones_no_leidas_count': no_leidas,
    }
