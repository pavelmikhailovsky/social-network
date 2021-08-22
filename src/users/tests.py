from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()

URL = '/api/v1.0/users/'


class CreateUsersTest(APITestCase):
    """
    API tests create users.
    """
    def setUp(self) -> None:
        User.objects.create(first_name='Weqeqwe', last_name='adsdaad', password='asdasdad')

    def test_create_users(self):
        response_anonymous = self.client.post(
            f'{URL}create/', {'first_name': 'name', 'last_name': 'testings', 'password': 'nametestings'}
        )
        token = self.client.post(f'{URL}token/login/', {'username': 'NameTestings', 'password': 'nametestings'})
        valid_token = token.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {valid_token}')
        response_authenticate = self.client.post(
            f'{URL}create/', {'first_name': 'names', 'last_name': 'testings', 'password': 'nametestings'}
        )
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response_anonymous.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_anonymous.data, {'status': 'created'})
        self.assertEqual(response_authenticate.status_code, status.HTTP_403_FORBIDDEN)


class OutputInformationUsersTests(APITestCase):
    """
    Tests output information o current user.
    """
    def setUp(self) -> None:
        User.objects.create(first_name='Test', last_name='Test', password=make_password('TestTest'))
        token = self.client.post(f'{URL}token/login/', {'username': 'TestTest', 'password': 'TestTest'})
        valid_token = token.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {valid_token}')

    def test_output_information(self):
        response = self.client.get(f'{URL}me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_settings(self):
        response = self.client.patch(f'{URL}me/partial-settings/', {'first_name': 'Testing'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Testing')
        self.assertEqual(response.data['username'], 'TestingTest')

    def test_remove_account(self):
        response = self.client.delete(f'{URL}me/remove-account/')
        self.assertEqual(response.data, {'status': 'deleted'})
