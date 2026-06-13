from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from biblioteca.models import Autor, Genero, Libro, Prestamo


class Command(BaseCommand):
    help = 'Crea grupos, permisos y un conjunto inicial de generos, autores y libros.'

    def handle(self, *args, **options):
        self.stdout.write('Creando grupos y permisos...')

        ct_prestamo = ContentType.objects.get_for_model(Prestamo)
        ct_libro = ContentType.objects.get_for_model(Libro)

        perm_add_prestamo = Permission.objects.get(content_type=ct_prestamo, codename='add_prestamo')
        perm_view_prestamo = Permission.objects.get(content_type=ct_prestamo, codename='view_prestamo')
        perm_change_prestamo = Permission.objects.get(content_type=ct_prestamo, codename='change_prestamo')
        perm_delete_prestamo = Permission.objects.get(content_type=ct_prestamo, codename='delete_prestamo')
        perm_view_libro = Permission.objects.get(content_type=ct_libro, codename='view_libro')

        grupo_socio, _ = Group.objects.get_or_create(name='socio')
        grupo_socio.permissions.set([perm_add_prestamo, perm_view_prestamo])
        self.stdout.write("  Grupo 'socio' listo")

        grupo_biblio, _ = Group.objects.get_or_create(name='bibliotecario')
        grupo_biblio.permissions.set([
            perm_add_prestamo,
            perm_view_prestamo,
            perm_change_prestamo,
            perm_delete_prestamo,
            perm_view_libro,
        ])
        self.stdout.write("  Grupo 'bibliotecario' listo")

        self.stdout.write('\nCreando generos...')
        generos_data = [
            'Novela', 'Ciencia Ficción', 'Historia', 'Poesía',
            'Terror', 'Filosofía', 'Biografía', 'Fantasía',
        ]
        generos = {}
        for nombre in generos_data:
            genero, _ = Genero.objects.get_or_create(nombre=nombre)
            generos[nombre] = genero
            self.stdout.write(f'  {nombre}')

        self.stdout.write('\nCreando autores...')
        autores_data = [
            ('Gabriel', 'García Márquez', 'Colombiana'),
            ('Isabel', 'Allende', 'Chilena'),
            ('Pablo', 'Neruda', 'Chilena'),
            ('Jorge Luis', 'Borges', 'Argentina'),
            ('Mario', 'Vargas Llosa', 'Peruana'),
            ('Julio', 'Cortázar', 'Argentina'),
            ('Stephen', 'King', 'Estadounidense'),
            ('George', 'Orwell', 'Británica'),
            ('Franz', 'Kafka', 'Checa'),
            ('Fyodor', 'Dostoevsky', 'Rusa'),
        ]
        autores = {}
        for nombre, apellido, nacionalidad in autores_data:
            autor, _ = Autor.objects.get_or_create(
                nombre=nombre,
                apellido=apellido,
                defaults={'nacionalidad': nacionalidad},
            )
            autores[apellido] = autor
            self.stdout.write(f'  {nombre} {apellido}')

        self.stdout.write('\nCreando libros...')
        libros_data = [
            ('Cien años de soledad', 'García Márquez', 'Novela', 1967, 3,
             'La historia de la familia Buendía a lo largo de siete generaciones en el pueblo ficticio de Macondo.',
             '1967-05-30'),
            ('La casa de los espíritus', 'Allende', 'Novela', 1982, 2,
             'Saga familiar que abarca cuatro generaciones de la familia Trueba en Chile.',
             '1982-01-01'),
            ('Veinte poemas de amor', 'Neruda', 'Poesía', 1924, 5,
             'Colección de poemas de amor del poeta chileno Pablo Neruda.',
             '1924-01-01'),
            ('Ficciones', 'Borges', 'Novela', 1944, 2,
             'Colección de cuentos que exploran laberintos, bibliotecas infinitas y paradojas del tiempo.',
             '1944-01-01'),
            ('La ciudad y los perros', 'Vargas Llosa', 'Novela', 1963, 3,
             'Novela ambientada en el Colegio Militar Leoncio Prado de Lima, Perú.',
             '1963-01-01'),
            ('Rayuela', 'Cortázar', 'Novela', 1963, 2,
             'Novela experimental que puede leerse en múltiples órdenes según instrucciones del autor.',
             '1963-06-28'),
            ('El resplandor', 'King', 'Terror', 1977, 4,
             'Un escritor acepta cuidar un hotel durante el invierno con su familia, con consecuencias aterradoras.',
             '1977-01-28'),
            ('1984', 'Orwell', 'Ciencia Ficción', 1949, 3,
             'Novela distópica sobre un régimen totalitario que controla todos los aspectos de la vida.',
             '1949-06-08'),
            ('La metamorfosis', 'Kafka', 'Novela', 1915, 4,
             'Gregor Samsa se despierta convertido en un insecto gigante y debe enfrentarse a su nueva realidad.',
             '1915-01-01'),
            ('Crimen y castigo', 'Dostoevsky', 'Novela', 1866, 2,
             'Un estudiante planea y ejecuta un crimen y debe lidiar con las consecuencias psicológicas.',
             '1866-01-01'),
            ('El otoño del patriarca', 'García Márquez', 'Novela', 1975, 1,
             'Retrato de un dictador latinoamericano que ha gobernado por más de cien años.',
             '1975-01-01'),
            ('Eva Luna', 'Allende', 'Novela', 1987, 3,
             'Historia de una mujer que narra su propia vida con el mismo poder con el que crea sus cuentos.',
             '1987-01-01'),
            ('Canto general', 'Neruda', 'Poesía', 1950, 2,
             'Poema épico que abarca la historia y geografía de América Latina.',
             '1950-01-01'),
            ('El Aleph', 'Borges', 'Fantasía', 1949, 3,
             'Colección de cuentos donde se incluye la famosa historia del punto que contiene todos los puntos.',
             '1949-01-01'),
            ('It', 'King', 'Terror', 1986, 2,
             'Un grupo de niños enfrenta a una entidad maligna que adopta la forma de sus peores miedos.',
             '1986-09-15'),
        ]

        for titulo, apellido_autor, genero_nombre, anio, stock, descripcion, publication_date in libros_data:
            autor = autores[apellido_autor]
            genero = generos[genero_nombre]
            libro, created = Libro.objects.get_or_create(
                titulo=titulo,
                defaults={
                    'autor': autor,
                    'genero': genero,
                    'anio': anio,
                    'stock': stock,
                    'descripcion': descripcion,
                    'publication_date': publication_date,
                },
            )
            estado = 'creado' if created else 'ya existe'
            self.stdout.write(f'  {titulo}: {estado}')

        self.stdout.write(self.style.SUCCESS('\nBase de datos inicial poblada correctamente'))
        self.stdout.write(f'Generos: {Genero.objects.count()}')
        self.stdout.write(f'Autores: {Autor.objects.count()}')
        self.stdout.write(f'Libros: {Libro.objects.count()}')
        self.stdout.write(f'Grupos: {Group.objects.count()}')
