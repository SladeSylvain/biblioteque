from django.urls import path

from . import views

app_name = 'reclamos'

urlpatterns = [
    # ============================================================
    # CLASE 1 — READ
    # ============================================================
    # Ruta para listar los reclamos del usuario autenticado.
    # Debe llamar a la vista views.lista_reclamos
    # Sugerencia de path: '' (raíz de la app)
    # Sugerencia de name: 'lista'
    #
    path('', views.lista_reclamos, name='lista'),

    # Ruta para ver el detalle de un reclamo específico.
    # Debe llamar a la vista views.detalle_reclamo
    # Recibe el id del reclamo como parámetro de la URL.
    # Sugerencia de path: 'reclamo/<int:id>/'
    # Sugerencia de name: 'detalle'
    #
    path('reclamo/<int:id>/', views.detalle_reclamo, name='detalle'),


    # ============================================================
    # CLASE 2 — CREATE / UPDATE
    # ============================================================
    # Ruta para crear un nuevo reclamo o sugerencia.
    # Debe llamar a la vista views.crear_reclamo
    # Sugerencia de path: 'crear/'
    # Sugerencia de name: 'crear'
    #
    path('crear/', views.crear_reclamo, name='crear'),

    # Ruta para editar un reclamo existente.
    # Debe llamar a la vista views.editar_reclamo
    # Recibe el id del reclamo a editar.
    # Sugerencia de path: 'reclamo/<int:id>/editar/'
    # Sugerencia de name: 'editar'
    #
    path('reclamo/<int:id>/editar/', views.editar_reclamo, name='editar'),


    # ============================================================
    # CLASE 3 — DELETE + PANEL BIBLIOTECARIO
    # ============================================================
    # Ruta para eliminar un reclamo (con confirmación previa).
    # Debe llamar a la vista views.eliminar_reclamo
    # Sugerencia de path: 'reclamo/<int:id>/eliminar/'
    # Sugerencia de name: 'eliminar'
    #
    path('reclamo/<int:id>/eliminar/', views.eliminar_reclamo, name='eliminar'),

    # Ruta para el panel del bibliotecario: ve todos los reclamos
    # de todos los usuarios y puede cambiar su estado.
    # Debe llamar a la vista views.panel_reclamos
    # Sugerencia de path: 'panel/'
    # Sugerencia de name: 'panel'
    #
    path('panel/', views.panel_reclamos, name='panel'),
]
