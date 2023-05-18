from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from users.models import Profile


class UserProfileTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='Test_user', password="123")

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.user.profile.phone_number = '+8988978979879'
        self.user.save()

    def test_data_profile(self):
        self.client.login(username='Test_user', password="123")
        avatar = self.user.profile.avatar
        self.assertEqual(avatar, "users/avatars/default/default_avatar1.png")


class RegistrationFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='Admin12', password='Pass123456')
        self.user.profile.phone_number = '+31231231231231'
        self.user.save()
        self.url = reverse_lazy('users:users_register')
        self.data1 = {
            'username': 'test_user',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test_user@example.com',
            'password1': 'Pass123456',
            'password2': 'Pass123456',
            'phone_number': '+1234567890'
        }

        self.data2 = {
            'username': 'test_user1',
            'first_name': 'Test1',
            'last_name': 'User1',
            'email': 'test_user@example.com',
            'password1': 'Pass123456',
            'password2': 'Pass123456',
            'phone_number': '+1234567890'
        }

    def test_registration_form(self):

        response = self.client.post(self.url, data=self.data1)
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username=self.data1['username'])
        self.assertEqual(user.first_name, self.data1['first_name'])
        self.assertEqual(user.last_name, self.data1['last_name'])
        self.assertEqual(user.email, self.data1['email'])
        self.assertEqual(user.profile.phone_number, self.data1['phone_number'])
        self.assertEqual(user.profile.avatar, "users/avatars/default/default_avatar1.png")

        response = self.client.post(self.url, data=self.data2)
        self.assertContains(response, 'Email test_user@example.com уже используется другим пользователем.')
        self.assertContains(response, '+1234567890 уже используется другим пользователем.')

    def test_login(self):
        login_data = {'username': 'Admin12',
                      'password': 'Pass123456'
                      }
        response = self.client.post(reverse_lazy('users:users_login'), login_data)

        self.assertEqual(response.status_code, 302)
        login_data2 = {'username': 'Admin12',
                      'password': 'Pass12345'
                      }

        response = self.client.get(reverse_lazy('users:users_logout'))
        response = self.client.post(reverse_lazy('users:users_login'), login_data2)
        self.assertContains(response, 'Please enter a correct username and password. '
                                      'Note that both fields may be case-sensitive.')




