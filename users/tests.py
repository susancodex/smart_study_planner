from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User


class AuthTests(TestCase):
	def setUp(self):
		self.client = APIClient()

	def test_register_and_login(self):
		# Register
		resp = self.client.post('/api/auth/register/', {'username': 'alice', 'password': 'StrongPass123!', 'email': 'a@example.com'}, format='json')
		self.assertEqual(resp.status_code, 201)
		# Login (obtain token)
		resp = self.client.post('/api/auth/login/', {'username': 'alice', 'password': 'StrongPass123!'}, format='json')
		self.assertEqual(resp.status_code, 200)
		self.assertIn('access', resp.data)

	def test_demo_credentials_endpoint(self):
		resp = self.client.get('/api/auth/demo/')
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.data['username'], 'susan')
		self.assertEqual(resp.data['password'], 'susan123')
		self.assertEqual(resp.data['email'], 'susanacharya.sp@gmail.com')

	def test_demo_user_can_login(self):
		self.client.get('/api/auth/demo/')
		resp = self.client.post('/api/auth/login/', {'username': 'susan', 'password': 'susan123'}, format='json')
		self.assertEqual(resp.status_code, 200)
		self.assertIn('access', resp.data)


class RootRouteTests(TestCase):
	def test_root_redirects_to_docs(self):
		resp = self.client.get('/')
		self.assertEqual(resp.status_code, 302)
		self.assertEqual(resp.url, '/api/docs/')
