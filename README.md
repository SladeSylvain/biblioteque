# Sistema de Biblioteca - Bootcamp Full Stack Python

Proyecto Django completo con autenticación, permisos y grupos.

## Instalación

```bash
# 1. Crear entorno virtual
python -m venv env

# 2. Activar entorno virtual
source env/bin/activate        # Mac/Linux
source env/Scripts/activate    # Windows Git Bash

# 3. Instalar dependencias
pip install -r requirements.txt

# 3.1 Instalar driver de PostgreSQL
pip install psycopg2-binary

# 4. Aplicar migraciones
python manage.py migrate

# 4.1 Poblar la bbdd con datos iniciales
python manage.py poblar_inicial

# 5. Crear superusuario
python manage.py createsuperuser


# 6. Iniciar el servidor
python manage.py runserver

```

## Que hace cada comando de carga

### 1. Datos iniciales del proyecto

```bash
python manage.py poblar_inicial
```

Este comando:

- crea grupos y permisos
- crea algunos generos
- crea algunos autores
- crea algunos libros

Importante:

- esto **no carga un archivo JSON**
- esto **no usa `loaddata`**
- esto sirve como poblado inicial rapido del proyecto
- reemplaza el uso manual de `python manage.py shell < poblar_db.py`

### 2. Respaldo del catalogo para alumnos

```bash
python manage.py exportar_catalogo
```

Este comando:

- genera un archivo JSON
- exporta solo el catalogo
- no incluye usuarios
- no incluye prestamos

Archivo generado por defecto:

```bash
fixtures/catalogo_alumnos.json
```

### 3. Cargar el respaldo JSON

```bash
python manage.py loaddata fixtures/catalogo_alumnos.json
```

Este comando:

- si carga el JSON
- inserta autores, editoriales, generos, tags, libros y revistas
- no crea usuarios ni prestamos

## Flujo recomendado

### Opcion A: poblar rapido con script Python

```bash
python manage.py migrate
python manage.py poblar_inicial
```

### Opcion B: cargar el catalogo completo para alumnos

```bash
python manage.py migrate
python manage.py loaddata fixtures/catalogo_alumnos.json
```

## URLs disponibles

| URL | Descripción | Acceso |
|-----|-------------|--------|
| `/` | Catálogo | Todos |
| `/libro/<id>/` | Detalle de libro | Todos |
| `/libro/<id>/solicitar/` | Solicitar préstamo de libro | Logueado |
| `/revista/<id>/` | Detalle de revista | Todos |
| `/revista/<id>/solicitar/` | Solicitar préstamo de revista | Logueado |
| `/mis-prestamos/` | Ver mis préstamos | Logueado |
| `/prestamo/<id>/devolver/` | Devolver préstamo | Logueado (dueño) |
| `/panel/` | Panel bibliotecario | Grupo bibliotecario |
| `/usuarios/registro/` | Registro de socio | Público |
| `/usuarios/perfil/` | Mi perfil | Logueado |
| `/login/` | Iniciar sesión | Público |
| `/logout/` | Cerrar sesión | Logueado |
| `/admin/` | Panel administración | Staff |

## Modelos

- **CustomUser** -> Socio con telefono, direccion, fecha_nacimiento
- **Genero** -> Nombre del genero literario
- **Autor** -> Nombre, apellido, nacionalidad
- **Tag** -> Etiquetas para libros y revistas
- **Editorial** -> Nombre, pais, anio de fundacion
- **Libro** -> Titulo, autor, genero, anio, stock, descripcion, fecha de publicacion, paginas
- **Revista** -> Titulo, editorial, numero de edicion, precio, fecha de publicacion, disponible, notas, paginas y tags
- **Prestamo** -> Socio, libro o revista, fecha_prestamo, fecha_devolucion, devuelto

## Grupos y permisos

| Grupo | Puede hacer |
|-------|-------------|
| socio | Ver libros, solicitar préstamo, ver sus préstamos |
| bibliotecario | Todo lo anterior + ver panel con todos los préstamos |
| admin/superuser | Acceso total |

## Migrar a PostgreSQL

Edita `config/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'biblioteca_db',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Luego instala el driver y aplica migraciones:
```bash
pip install psycopg2-binary
python manage.py migrate
```

## Respaldo para alumnos

Si quieres compartir la base con tus alumnos, pero sin usuarios ni prestamos, usa este comando:

```bash
python manage.py exportar_catalogo
```

Eso genera este archivo:

```bash
fixtures/catalogo_alumnos.json
```

Incluye:

- Genero
- Autor
- Tag
- Editorial
- Libro
- Revista

Excluye:

- usuarios.CustomUser
- biblioteca.Prestamo

Si quieres restaurarlo en otra base:

```bash
python manage.py loaddata fixtures/catalogo_alumnos.json
```

Tambien puedes indicar otra ruta de salida:

```bash
python manage.py exportar_catalogo --output respaldo/catalogo.json
```
