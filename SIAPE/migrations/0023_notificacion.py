import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SIAPE', '0022_decisiondocenteajuste'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notificacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rol_destino', models.CharField(max_length=100)),
                ('tipo', models.CharField(choices=[('nuevo_caso', 'Nuevo caso'), ('devolucion', 'Devolución'), ('comentario_docente', 'Comentario del docente')], max_length=30)),
                ('titulo', models.CharField(max_length=191)),
                ('mensaje', models.TextField(blank=True, default='')),
                ('leida', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('solicitud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notificaciones', to='SIAPE.solicitudes')),
            ],
            options={
                'db_table': 'notificaciones',
                'ordering': ['-created_at'],
            },
        ),
    ]
