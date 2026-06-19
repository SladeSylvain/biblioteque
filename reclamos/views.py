from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import Reclamo  # Asegúrate de que el modelo esté importado
from .forms import ReclamoForm  # Reemplaza por el nombre real de tu formulario si varía

# ============================================================
# CLASE 1 — READ
# ============================================================

"""
Lista únicamente los reclamos del usuario autenticado (request.user).

Pasos esperados:
1. Filtrar Reclamo.objects con usuario=request.user
2. Renderizar 'reclamos/lista.html' pasando esos reclamos en el contexto

Pista: no muestres TODOS los reclamos, solo los del usuario logueado.
Eso se hace con .filter(usuario=request.user)
"""

@login_required
def lista_reclamos(request):
   reclamos = Reclamo.objects.filter(usuario=request.user)
   return render(request, 'reclamos/lista.html', {'reclamos': reclamos})


"""
Muestra el detalle de un reclamo específico.

Pasos esperados:
1. Buscar el reclamo por id usando get_object_or_404
2. Verificar que el reclamo pertenezca al usuario autenticado
   (si no es el dueño, no debería poder verlo)
3. Renderizar 'reclamos/detalle.html' con el reclamo en el contexto

Pista: get_object_or_404(Reclamo, id=id, usuario=request.user)
ya filtra y da 404 si no es del usuario, en una sola línea.
"""
@login_required
def detalle_reclamo(request, id):
   reclamo = get_object_or_404(Reclamo, id=id, usuario=request.user)
   #reclamo = Reclamo.objects.get(id=id, usuario=request.user)
   return render(request, 'reclamos/detalle.html', {'reclamo': reclamo})

# ============================================================
# CLASE 2 — CREATE / UPDATE
# ============================================================

"""
Crea un nuevo reclamo o sugerencia para el usuario autenticado.

Pasos esperados:
1. Si request.method == 'POST':
   - Leer 'tipo', 'titulo', 'descripcion' desde request.POST
   - Crear el Reclamo con Reclamo.objects.create(...)
   asignando usuario=request.user (NO pedirlo en el formulario)
   - Redirigir a la lista de reclamos
2. Si es GET, renderizar 'reclamos/form.html' (formulario vacío)

Pista: el campo 'usuario' nunca debe venir del formulario.
Siempre se asigna desde request.user por seguridad.
"""
@login_required
def crear_reclamo(request):
   if request.method == 'POST':
      tipo = request.POST['tipo']
      titulo = request.POST['titulo']
      descripcion = request.POST['descripcion']

      Reclamo.objects.create(
         usuario=request.user,
         tipo=tipo,
         titulo=titulo,
         descripcion=descripcion,
      )
      return redirect('reclamos:lista')
   return render(request, 'reclamos/form.html')

@login_required
def editar_reclamo(request, id):
    # Paso 5 (Seguridad): Buscamos el reclamo asegurando que pertenezca al usuario logueado
    reclamo = get_object_or_404(Reclamo, id=id, usuario=request.user)
    
    if request.method == 'POST':
        # Instanciamos el formulario con los datos enviados y el reclamo actual a modificar
        form = ReclamoForm(request.POST, instance=reclamo)
        if form.is_valid():
            form.save()
            # Redirigimos al detalle del reclamo ya modificado
            return redirect('reclamos:detalle', id=reclamo.id)
    else:
        # GET: Pre-cargamos el formulario con los datos actuales del reclamo
        form = ReclamoForm(instance=reclamo)
        
    return render(request, 'reclamos/form.html', {
        'form': form,
        'reclamo': reclamo,
        'es_edicion': True  # Útil si tu form.html usa una condicional para cambiar el título
    })


# ============================================================
# CLASE 3 — DELETE + PANEL BIBLIOTECARIO
# ============================================================

@login_required
def eliminar_reclamo(request, id):
    # Seguridad: Buscamos el reclamo asegurando que pertenezca al usuario logueado
    reclamo = get_object_or_404(Reclamo, id=id, usuario=request.user)

    if request.method == 'POST':
        reclamo.delete()
        # IMPORTANTE: Debes devolver una redirección después de borrar
        return redirect('reclamos:lista') 

    # Si es GET, debes devolver la renderización del template de confirmación
    return render(request, 'reclamos/confirmar_eliminar.html', {'reclamo': reclamo})


@login_required
@permission_required('reclamos.change_reclamo', raise_exception=True)
def panel_reclamos(request):
    if request.method == 'POST':
        reclamo_id = request.POST.get('reclamo_id')
        nuevo_estado = request.POST.get('estado')
        reclamo = get_object_or_404(Reclamo, id=reclamo_id)
        reclamo.estado = nuevo_estado
        reclamo.save()
        return redirect('reclamos:panel')

    reclamos = Reclamo.objects.select_related('usuario').all()
    return render(request, 'reclamos/panel.html', {'reclamos': reclamos})
