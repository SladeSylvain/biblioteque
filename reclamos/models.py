from django.conf import settings
from django.db import models


class Reclamo(models.Model):
    TIPO_CHOICES = [
        ('reclamo', 'Reclamo'),
        ('sugerencia', 'Sugerencia'),
    ]

    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_revision', 'En revisión'),
        ('resuelto', 'Resuelto'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reclamos'
    )
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='reclamo')
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField(max_length=1000)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name_plural = 'Reclamos y sugerencias'

    def __str__(self):
        return f'{self.get_tipo_display()}: {self.titulo} ({self.usuario.username})'
