from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import StudyPlan
from datetime import date, timedelta


class PlannerPermissionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_a = User.objects.create_user(username='usera', password='testpass')
        self.user_b = User.objects.create_user(username='userb', password='testpass')
        # create a study plan for user_b
        self.plan_b = StudyPlan.objects.create(
            user=self.user_b,
            title='B Plan',
            description='desc',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=7),
        )

    def authenticate(self, user):
        resp = self.client.post('/api/auth/login/', {'username': user.username, 'password': 'testpass'}, format='json')
        token = resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_user_cannot_delete_another_users_plan(self):
        # login as user_a
        self.authenticate(self.user_a)
        # attempt to delete user_b's plan
        url = f'/api/planner/studyplans/{self.plan_b.id}/'
        resp = self.client.delete(url)
        # should be 404 because queryset filters by request.user, or 403 if object-level checks run
        self.assertIn(resp.status_code, (403, 404))
