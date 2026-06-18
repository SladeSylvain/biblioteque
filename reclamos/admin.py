from django.contrib import admin

from .models import Reclamo


@admin.register(Reclamo)
class ReclamoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'tipo', 'estado', 'fecha_creacion')
    list_filter = ('tipo', 'estado')
    search_fields = ('titulo', 'descripcion', 'usuario__username')
