from django.urls import reverse
from rest_framework.test import APITestCase, force_authenticate, APIRequestFactory, APIClient

from ..models import User


class RegisterViewTest(APITestCase):
    def setUp(self):
        self.register_url = reverse('users:user-register')
        self.user_data = {
            'email': 'testuser@gmail.com',
            'password': 'Secret23',
            'password2': 'Secret23',
            'first_name': 'John',
            'patronymic': 'Pablo',
            'last_name': 'Starykh',
        }

    def test_register_correct(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, 201, 'User is not registered')
        email = self.user_data['email']
        self.assertTrue(User.objects.get(email=email), 'User is not added to the database')

    def test_register_without_password2(self):
        self.user_data.pop('password2')
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, 400, 'User is registered without password2')

    def test_register_without_email(self):
        self.user_data.pop('email')
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, 400, 'User is registered without email')

    def test_register_without_first_name(self):
        self.user_data.pop('first_name')
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, 400, 'User is registered without first_name')

    def test_register_without_last_name(self):
        self.user_data.pop('last_name')
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, 400, 'User is registered without last_name')


class ChangePasswordViewTest(APITestCase):

    def setUp(self):
        self.email = 'testuser@gmail.com'
        self.password = 'Secret23'
        extra_fields = {'first_name': 'John', 'patronymic': 'Pablo', 'last_name': 'Starykh'}
        self.user = User.objects.create_user(email=self.email, password=self.password, **extra_fields)
        self.new_password = 'dfjg0FFEF'
        self.new_password_data = {
            'old_password': self.password, 'password': self.new_password,
            'password2': self.new_password
        }
        self.change_password_url = reverse('users:user-change-password', kwargs={'pk': self.user.pk})

    def test_change_password_correct(self):

        auth_client = APIClient()
        auth_client.force_authenticate(user=self.user)
        response = auth_client.put(self.change_password_url, self.new_password_data, format='json')
        self.assertEqual(response.status_code, 200, 'Password has not been changed')

    def test_change_another_user(self):
        new_user = User.objects.create_user(email='test@gmail.com', password=self.password)
        auth_client = APIClient()
        auth_client.force_authenticate(user=new_user)
        response = auth_client.put(self.change_password_url, self.new_password_data, format='json')
        self.assertEqual(response.status_code, 400, 'Password changed by another user')


class UpdateProfileViewTest(APITestCase):

    def setUp(self):
        self.email = 'testuser@gmail.com'
        self.password = 'Secret23'
        extra_fields = {'first_name': 'John', 'patronymic': 'Pablo', 'last_name': 'Starykh'}
        new_extra_fields = {'first_name': 'John', 'patronymic': 'Pablo', 'last_name': 'Starykh'}

        self.user = User.objects.create_user(email=self.email, password=self.password, **extra_fields)
        self.new_profile_data = {
            'email': self.email, 'first_name': new_extra_fields['first_name'],
            'last_name': new_extra_fields['last_name'], 'patronymic': new_extra_fields['last_name']
        }
        self.update_profile_url = reverse('users:user-update-profile', kwargs={'pk': self.user.pk})

    def test_update_profile_correct(self):

        auth_client = APIClient()
        auth_client.force_authenticate(user=self.user)
        response = auth_client.put(self.update_profile_url, self.new_profile_data, format='json')
        self.assertEqual(response.status_code, 200, 'Profile has not been changed')

    def test_update_profile_without_email_correct(self):
        self.new_profile_data.pop('email')
        auth_client = APIClient()
        auth_client.force_authenticate(user=self.user)
        response = auth_client.put(self.update_profile_url, self.new_profile_data, format='json')
        self.assertEqual(response.status_code, 400, 'Profile updated without email')

    def test_update_profile_without_first_name_correct(self):
        self.new_profile_data.pop('first_name')
        auth_client = APIClient()
        auth_client.force_authenticate(user=self.user)
        response = auth_client.put(self.update_profile_url, self.new_profile_data, format='json')
        self.assertEqual(response.status_code, 400, 'Profile updated without first name')

    def test_update_profile_without_last_name_correct(self):
        self.new_profile_data.pop('last_name')
        auth_client = APIClient()
        auth_client.force_authenticate(user=self.user)
        response = auth_client.put(self.update_profile_url, self.new_profile_data, format='json')
        self.assertEqual(response.status_code, 400, 'Profile updated without last name')

    def test_update_profile_another_user(self):
        new_user = User.objects.create_user(email='test@gmail.com', password=self.password)
        auth_client = APIClient()
        auth_client.force_authenticate(user=new_user)
        response = auth_client.put(self.update_profile_url, self.new_profile_data, format='json')
        self.assertEqual(response.status_code, 400, 'Profile updated by another user')
