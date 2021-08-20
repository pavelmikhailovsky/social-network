from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase

from . import views

User = get_user_model()


class UserModelTests(TestCase):
    def test_username_field(self):
        create_user = User.objects.create(
            first_name='Admin', last_name='Admin', password='AdminAdmin', username='AdminAdmin'
        )
        self.assertEqual(create_user.username, 'AdminAdmin')


class EndpointTests(APITestCase):
    def test_create_users(self):
        response = self.client.post('/api/v1.0/users/create/', {'username': 'User Test', 'password': 'UserTest'})

