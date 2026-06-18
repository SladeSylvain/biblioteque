from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reclamo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('reclamo', 'Reclamo'), ('sugerencia', 'Sugerencia')], default='reclamo', max_length=20)),
                ('titulo', models.CharField(max_length=150)),
                ('descripcion', models.TextField(max_length=1000)),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('en_revision', 'En revisión'), ('resuelto', 'Resuelto')], default='pendiente', max_length=20)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reclamos', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Reclamos y sugerencias',
                'ordering': ['-fecha_creacion'],
            },
        ),
    ]
