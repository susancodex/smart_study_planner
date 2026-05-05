from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User


class AuthTests(TestCase):
	def setUp(self):
		self.client = APIClient()

	def test_register_and_login(self):
		# Register
		resp = self.client.post('/api/auth/register/', {'username': 'alice', 'password': 'pass1234', 'email': 'a@example.com'}, format='json')
		self.assertEqual(resp.status_code, 201)
		# Login (obtain token)
		resp = self.client.post('/api/auth/login/', {'username': 'alice', 'password': 'pass1234'}, format='json')
		self.assertEqual(resp.status_code, 200)
		self.assertIn('access', resp.data)
