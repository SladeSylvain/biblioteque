# App "reclamos" — CRUD desde cero

Esta app está pre-armada (modelo, migración, admin) para que te concentres
en lo que importa en este módulo: **views.py** y **completar los templates**.

## Instalación en el proyecto biblioteca

1. Copia la carpeta `reclamos/` dentro de la raíz de tu proyecto
   (al mismo nivel que las apps `biblioteca` y `usuarios`).

2. Registra la app en `config/settings.py`, dentro de `INSTALLED_APPS`:

   ```python
   INSTALLED_APPS = [
       ...
       'biblioteca',
       'usuarios',
       'reclamos',   # ← agregar esta línea
   ]
   ```

3. Conecta las URLs de la app en `config/urls.py` (el de la raíz del proyecto):

   ```python
   urlpatterns = [
       ...
       path('reclamos/', include('reclamos.urls')),
   ]
   ```

4. Aplica la migración (ya viene escrita, no necesitas correr `makemigrations`):

   ```bash
   python manage.py migrate
   ```

5. Verifica que la tabla se creó:

   ```bash
   python manage.py showmigrations reclamos
   ```

   Deberías ver `[X] 0001_initial`.

## Qué está listo y qué falta

| Archivo | Estado |
|---|---|
| `models.py` | ✅ Completo |
| `migrations/0001_initial.py` | ✅ Completo |
| `admin.py` | ✅ Completo |
| `apps.py` | ✅ Completo |
| `urls.py` | 🟡 Estructura lista, rutas comentadas — descomentar a medida que avances |
| `views.py` | 🔴 Vacío con docstrings — esto es tu ejercicio principal (Clases 1, 2 y 3) |
| `templates/reclamos/*.html` | 🟡 Estructura y estilos listos, partes con `TODO` para completar (Ejercicio 2 de cada clase) |

## Orden de trabajo sugerido

**Clase 1 (Read):**
1. Completa `lista_reclamos` y `detalle_reclamo` en `views.py`
2. Descomenta las rutas de Clase 1 en `urls.py`
3. Completa los `TODO` de `lista.html` y `detalle.html`

**Clase 2 (Create/Update):**
1. Completa `crear_reclamo` y `editar_reclamo` en `views.py`
2. Descomenta las rutas de Clase 2 en `urls.py`
3. `form.html` ya está armado — solo verifica que los `name` de los inputs coincidan con lo que lees en tu vista

**Clase 3 (Delete + Panel):**
1. Completa `eliminar_reclamo` y `panel_reclamos` en `views.py`
2. Descomenta las rutas de Clase 3 en `urls.py`
3. Completa los `TODO` de `confirmar_eliminar.html` y `panel.html`
4. Para probar el panel necesitas un usuario con el permiso `reclamos.change_reclamo`
   (asignable desde el admin de Django, en el grupo o usuario correspondiente)

## Notas importantes

- El campo `usuario` de `Reclamo` **nunca** debe venir de un formulario — siempre
  se asigna con `request.user` en la vista, por seguridad.
- Las vistas de detalle, editar y eliminar deben verificar que el reclamo
  pertenezca al usuario autenticado (excepto el panel del bibliotecario,
  que sí ve todos).
- Todas las vistas llevan `@login_required` — un usuario no autenticado
  no debería poder acceder a ninguna de ellas.
