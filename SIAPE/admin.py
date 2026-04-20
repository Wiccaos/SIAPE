from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Usuario, Roles, Areas, CategoriasAjustes, PerfilUsuario, Carreras, Estudiantes, Solicitudes,
    Evidencias, Asignaturas, AsignaturasEnCurso, Entrevistas, AjusteRazonable, AjusteAsignado, HorarioBloqueado,
    Notificacion, ComentarioDocenteHistorial,
)

try:
    admin.site.unregister(Usuario)
except admin.sites.NotRegistered:
    pass

@admin.register(Usuario)
class CustomUserAdmin(UserAdmin):
    """
    Configuración personalizada del Admin para el modelo Usuario.
    """

    list_display = ('email', 'first_name', 'last_name', 'rut', 'is_staff')
    
    search_fields = ('email', 'first_name', 'last_name', 'rut')
    
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información Personal', {'fields': ('first_name', 'last_name', 'rut', 'numero')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password2', 'first_name', 'last_name', 'rut', 'is_staff', 'is_superuser'),
        }),
    )
    
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(Roles)
admin.site.register(Areas)
admin.site.register(CategoriasAjustes)
admin.site.register(PerfilUsuario)
admin.site.register(Carreras)
admin.site.register(Estudiantes)
admin.site.register(Solicitudes)
admin.site.register(Evidencias)
admin.site.register(Asignaturas)
admin.site.register(AsignaturasEnCurso)
admin.site.register(Entrevistas)
admin.site.register(AjusteRazonable)
admin.site.register(AjusteAsignado)
admin.site.register(HorarioBloqueado)


@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo', 'rol_destino', 'titulo', 'leida', 'created_at', 'solicitud_id')
    list_filter = ('tipo', 'rol_destino', 'leida')
    search_fields = ('titulo', 'mensaje')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ComentarioDocenteHistorial)
class ComentarioDocenteHistorialAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'tipo', 'solicitud_id', 'docente', 'texto_preview')
    list_filter = ('tipo',)
    search_fields = ('texto',)
    readonly_fields = ('created_at',)

    def texto_preview(self, obj):
        return (obj.texto or '')[:80]