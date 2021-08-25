from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()

URL = '/api/v1.0/users'


class CreateUsersTest(APITestCase):
    """
    Tests create users.
    """
    def setUp(self) -> None:
        User.objects.create(first_name='Weqeqwe', last_name='adsdaad', password='asdasdad')

    def test_create_users(self):
        response_anonymous = self.client.post(
            f'{URL}/create/', {'first_name': 'name', 'last_name': 'testings', 'password': 'nametestings'}
        )
        token = self.client.post(f'{URL}/token/login/', {'username': 'NameTestings', 'password': 'nametestings'})
        valid_token = token.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {valid_token}')
        response_authenticate = self.client.post(
            f'{URL}/create/', {'first_name': 'names', 'last_name': 'testings', 'password': 'nametestings'}
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
        token = self.client.post(f'{URL}/token/login/', {'username': 'TestTest', 'password': 'TestTest'})
        valid_token = token.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {valid_token}')

    def test_output_information(self):
        response = self.client.get(f'{URL}/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_settings(self):
        response = self.client.patch(f'{URL}/me/partial-settings/', {'first_name': 'Testing'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Testing')
        self.assertEqual(response.data['username'], 'TestingTest')

    def test_remove_account(self):
        response = self.client.delete(f'{URL}/me/remove-account/')
        self.assertEqual(response.data, {'status': 'deleted'})


class GetUsersTests(APITestCase):
    def setUp(self) -> None:
        self.user_subscriber = User.objects.create(
            first_name='UserSubscriber', last_name='User', password=make_password('UserUser')
        )
        self.user = User.objects.create(first_name='User', last_name='User', password=make_password('UserUser'))
        self.token = self.client.post(f'{URL}/token/login/', {'username': 'UsersubscriberUser', 'password': 'UserUser'})
        self.valid_token = self.token.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.valid_token}')

    def test_information_viewed_profile(self):
        response = self.client.get(f'{URL}/{self.user.id}/')
        check_subscriber = self.client.get(f'{URL}/{self.user.id}/check-subscriber/')
        self.client.credentials()
        check_subscriber_anonymous_user = self.client.get(f'{URL}/{self.user.id}/check-subscriber/')
        self.assertEqual(check_subscriber.data, {'subscriber': False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(check_subscriber_anonymous_user.data, {'status': 'not authorization'})

    def test_follow_unfollow_on_user(self):
        response_subscribe = self.client.get(f'{URL}/{self.user.id}/follow/')
        check_follow = self.client.get(f'{URL}/{self.user.id}/check-follow/')
        response_unsubscribe = self.client.get(f'{URL}/{self.user.id}/follow/')
        check_unfollow = self.client.get(f'{URL}/{self.user.id}/check-follow/')
        self.assertEqual(response_subscribe.data, {'status': 'subscribed'})
        self.assertEqual(check_follow.data, {'follow': True})
        self.assertEqual(response_unsubscribe.data, {'status': 'unsubscribed'})
        self.assertEqual(check_unfollow.data, {'follow': False})

    def test_destroy_users_account(self):
        response_not_staff = self.client.delete(f'{URL}/{self.user.id}/')
        User.objects.create(
            first_name='Admin', last_name='Admin', password=make_password('AdminAdmin'), is_staff=True
        )
        token = self.client.post(f'{URL}/token/login/', {'username': 'AdminAdmin', 'password': 'AdminAdmin'})
        valid_token = token.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {valid_token}')
        response_is_staff = self.client.delete(f'{URL}/{self.user.id}/')
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response_not_staff.data, {'permission error': 'user is not staff'})
        self.assertEqual(response_is_staff.data, {'status': 'deleted'})






