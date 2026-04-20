from .models import Notificacion


def notificaciones_usuario(request):
    if not request.user.is_authenticated:
        return {'notificaciones_header': [], 'notificaciones_no_leidas_count': 0}

    try:
        rol_nombre = request.user.perfil.rol.nombre_rol
    except AttributeError:
        return {'notificaciones_header': [], 'notificaciones_no_leidas_count': 0}

    notificaciones_qs = Notificacion.objects.filter(rol_destino=rol_nombre).select_related('solicitud')
    notificaciones_header = list(notificaciones_qs[:8])
    no_leidas_count = notificaciones_qs.filter(leida=False).count()

    return {
        'notificaciones_header': notificaciones_header,
        'notificaciones_no_leidas_count': no_leidas_count,
    }
