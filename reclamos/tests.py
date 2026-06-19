from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from .models import Reclamo

User = get_user_model()

class ReclamosTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='jose', password='password123', first_name='José', last_name='Pérez')
        self.user2 = User.objects.create_user(username='maria', password='password123', first_name='María', last_name='Gómez')
        
        # Create a librarian user
        self.librarian = User.objects.create_user(username='librarian', password='password123', is_staff=True)
        # Give librarian permission to change reclamos
        change_permission = Permission.objects.get(codename='change_reclamo')
        self.librarian.user_permissions.add(change_permission)

        # Create claims
        self.reclamo1 = Reclamo.objects.create(
            usuario=self.user1,
            tipo='reclamo',
            titulo='Falta libro de Kafka',
            descripcion='No encuentro La metamorfosis en el estante.'
        )
        self.reclamo2 = Reclamo.objects.create(
            usuario=self.user2,
            tipo='sugerencia',
            titulo='Más sillones',
            descripcion='Sería bueno tener más sillones cómodos.'
        )

    def test_lista_reclamos_requires_login(self):
        response = self.client.get(reverse('reclamos:lista'))
        self.assertEqual(response.status_code, 302) # Redirect to login

    def test_lista_reclamos_shows_only_user_claims(self):
        self.client.login(username='jose', password='password123')
        response = self.client.get(reverse('reclamos:lista'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Falta libro de Kafka')
        self.assertNotContains(response, 'Más sillones')

    def test_detalle_reclamo_owner_access(self):
        self.client.login(username='jose', password='password123')
        response = self.client.get(reverse('reclamos:detalle', args=[self.reclamo1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'José Pérez')
        self.assertContains(response, '(jose)')
        self.assertContains(response, 'Falta libro de Kafka')

    def test_detalle_reclamo_non_owner_access_denied(self):
        self.client.login(username='maria', password='password123')
        response = self.client.get(reverse('reclamos:detalle', args=[self.reclamo1.id]))
        self.assertEqual(response.status_code, 404)

    def test_crear_reclamo(self):
        self.client.login(username='jose', password='password123')
        response = self.client.post(reverse('reclamos:crear'), {
            'tipo': 'sugerencia',
            'titulo': 'Nueva sugerencia',
            'descripcion': 'Descripción de prueba'
        })
        self.assertEqual(response.status_code, 302) # Redirects to list
        self.assertTrue(Reclamo.objects.filter(titulo='Nueva sugerencia', usuario=self.user1).exists())

    def test_editar_reclamo_owner(self):
        self.client.login(username='jose', password='password123')
        response = self.client.post(reverse('reclamos:editar', args=[self.reclamo1.id]), {
            'tipo': 'reclamo',
            'titulo': 'Falta libro de Kafka MODIFICADO',
            'descripcion': 'Nueva descripción'
        })
        self.assertEqual(response.status_code, 302)
        self.reclamo1.refresh_from_db()
        self.assertEqual(self.reclamo1.titulo, 'Falta libro de Kafka MODIFICADO')

    def test_editar_reclamo_non_owner(self):
        self.client.login(username='maria', password='password123')
        response = self.client.post(reverse('reclamos:editar', args=[self.reclamo1.id]), {
            'tipo': 'reclamo',
            'titulo': 'Intento hackeo',
            'descripcion': 'Intento hackeo'
        })
        self.assertEqual(response.status_code, 404)

    def test_eliminar_reclamo_owner(self):
        self.client.login(username='jose', password='password123')
        response = self.client.post(reverse('reclamos:eliminar', args=[self.reclamo1.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Reclamo.objects.filter(id=self.reclamo1.id).exists())

    def test_eliminar_reclamo_non_owner(self):
        self.client.login(username='maria', password='password123')
        response = self.client.post(reverse('reclamos:eliminar', args=[self.reclamo1.id]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Reclamo.objects.filter(id=self.reclamo1.id).exists())

    def test_panel_reclamos_permission(self):
        # Regular user cannot access
        self.client.login(username='jose', password='password123')
        response = self.client.get(reverse('reclamos:panel'))
        self.assertEqual(response.status_code, 403) # Forbidden

        # Librarian can access
        self.client.login(username='librarian', password='password123')
        response = self.client.get(reverse('reclamos:panel'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Falta libro de Kafka')
        self.assertContains(response, 'Más sillones')
        self.assertContains(response, 'José Pérez')
        self.assertContains(response, 'María Gómez')

    def test_panel_reclamos_update_status(self):
        self.client.login(username='librarian', password='password123')
        response = self.client.post(reverse('reclamos:panel'), {
            'reclamo_id': self.reclamo1.id,
            'estado': 'en_revision'
        })
        self.assertEqual(response.status_code, 302)
        self.reclamo1.refresh_from_db()
        self.assertEqual(self.reclamo1.estado, 'en_revision')
