import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


def backfill_historial_docente(apps, schema_editor):
    Historial = apps.get_model('SIAPE', 'ComentarioDocenteHistorial')
    AjusteAsignado = apps.get_model('SIAPE', 'AjusteAsignado')
    DecisionDocenteAjuste = apps.get_model('SIAPE', 'DecisionDocenteAjuste')

    for adj in AjusteAsignado.objects.exclude(comentarios_docente='').select_related(
        'solicitudes', 'docente_comentador'
    ):
        if not adj.docente_comentador_id:
            continue
        fecha = adj.fecha_comentario_docente or django.utils.timezone.now()
        Historial.objects.create(
            solicitud_id=adj.solicitudes_id,
            ajuste_asignado_id=adj.id,
            docente_id=adj.docente_comentador_id,
            tipo='observacion',
            decision_codigo='',
            texto=adj.comentarios_docente[:8000],
            created_at=fecha,
        )

    for dec in DecisionDocenteAjuste.objects.select_related(
        'ajuste_asignado', 'docente'
    ):
        adj = dec.ajuste_asignado
        com = (dec.comentario or '').strip()
        if dec.decision == 'aprobado' and not com:
            texto = 'Aprobó el ajuste sin comentario adicional.'
        elif dec.decision == 'rechazado' and not com:
            texto = 'Rechazó el ajuste.'
        else:
            disp = 'Aprobado' if dec.decision == 'aprobado' else 'Rechazado'
            texto = f'Decisión: {disp}. {com}'.strip()
        Historial.objects.create(
            solicitud_id=adj.solicitudes_id,
            ajuste_asignado_id=adj.id,
            docente_id=dec.docente_id,
            tipo='decision',
            decision_codigo=dec.decision,
            texto=texto[:8000],
            created_at=dec.fecha_decision,
        )


class Migration(migrations.Migration):

    dependencies = [
        ('SIAPE', '0024_remove_decisiondocenteajuste_unique_decision_docente_ajuste_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComentarioDocenteHistorial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('observacion', 'Observación al equipo'), ('decision', 'Decisión sobre ajuste')], max_length=20)),
                ('decision_codigo', models.CharField(blank=True, default='', help_text='aprobado/rechazado solo si tipo es decisión', max_length=15, verbose_name='Código decisión')),
                ('texto', models.TextField()),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('ajuste_asignado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historial_comentarios_docente', to='SIAPE.ajusteasignado')),
                ('docente', models.ForeignKey(limit_choices_to={'rol__nombre_rol': 'Docente'}, on_delete=django.db.models.deletion.CASCADE, related_name='comentarios_docente_historial', to='SIAPE.perfilusuario')),
                ('solicitud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historial_comentarios_docente', to='SIAPE.solicitudes')),
            ],
            options={
                'db_table': 'comentario_docente_historial',
                'ordering': ['-created_at'],
            },
        ),
        migrations.RunPython(backfill_historial_docente, migrations.RunPython.noop),
    ]
