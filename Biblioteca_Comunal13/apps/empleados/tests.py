from django.test import TestCase
from django.urls import reverse
from apps.empleados.models import Empleado, EmpleadoManager
from typing import cast


class RegistrationTests(TestCase):
	def setUp(self):
		self.url = reverse('register')

	def test_register_success(self):
		data = {
			'dni': '12345678',
			'nombre': 'Juan',
			'apellido': 'Perez',
			'email': 'juan@example.com',
			'telefono': '123456789',
			'password': 'secret123',
			'confirm_password': 'secret123',
		}
		resp = self.client.post(self.url, data)
		# Redirige al index
		self.assertEqual(resp.status_code, 302)
		self.assertTrue(Empleado.objects.filter(dni='12345678').exists())

	def test_register_password_mismatch(self):
		data = {
			'dni': '87654321',
			'nombre': 'Ana',
			'apellido': 'Lopez',
			'email': 'ana@example.com',
			'telefono': '987654321',
			'password': 'abc123',
			'confirm_password': 'different',
		}
		resp = self.client.post(self.url, data)
		# No redirige; debería re-renderizar la página con error
		self.assertEqual(resp.status_code, 200)
		self.assertContains(resp, 'Las contraseñas no coinciden')

	def test_register_duplicate_dni(self):
		cast(EmpleadoManager, Empleado.objects).create_user(dni='55555555', password='p')
		data = {
			'dni': '55555555',
			'nombre': 'Dup',
			'apellido': 'User',
			'email': 'dup@example.com',
			'telefono': '000',
			'password': 'pass123',
			'confirm_password': 'pass123',
		}
		resp = self.client.post(self.url, data)
		self.assertEqual(resp.status_code, 200)
		self.assertContains(resp, 'Ya existe un usuario con ese DNI')
