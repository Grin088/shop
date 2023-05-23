from django.test import TestCase
from django.urls import reverse_lazy
from users.models import CustomUser


class UserProfileTest(TestCase):
    """Создание профиля"""

    @classmethod
    def setUpClass(cls):
        """Создание пользователя"""
        super().setUpClass()
        cls.user = CustomUser.objects.create_user(username='test_user', email='test1@admin.com', password="123")

    @classmethod
    def tearDownClass(cls):
        """ Удаление пользователя"""
        super().tearDownClass()
        cls.user.delete()

    def test_custom_user_data(self):
        """Проверка данных профиля созданного пользователя"""

        self.client.login(username='Test_user', password="123")
        avatar = self.user.avatar
        phone = self.user.phone_number
        self.assertEqual(avatar, "users/avatars/default/default_avatar1.png")
        self.assertEqual(phone, '+0000000000')


class RegistrationFormTest(TestCase):
    """ Проверка страницы регистрации и входа """

    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test_user@example.com',
                                                   username='Admin12',
                                                   password='Pass123456')

        self.url = reverse_lazy('users:users_register')
        self.data1 = {
            'username': 'test_user',
            'email': 'test_user22@example.com',
            'password1': 'Pass123456',
            'password2': 'Pass123456',
        }

        self.data2 = {
            'username': 'test_user1',
            'first_name': 'Test1',
            'last_name': 'User1',
            'email': 'Test_user@example.com',
            'password1': 'Pass123456',
            'password2': 'Pass123456',
        }

    def tearDown(self) -> None:
        self.user.delete()

    def test_registration_form(self):
        """Проверка формы регистрации"""
        response = self.client.post(self.url, data=self.data1)
        self.assertEqual(response.status_code, 302)
        user = CustomUser.objects.get(username=self.data1['username'])
        self.assertEqual(user.email, self.data1['email'])
        self.assertEqual(user.phone_number, '+0000000000')
        self.assertEqual(user.avatar, "users/avatars/default/default_avatar1.png")

    def test_login(self):
        """Проверка входа """
        login_data = {'username': 'test_user@example.com',
                      'password': 'Pass123456'
                      }
        response = self.client.post(reverse_lazy('users:users_login'), login_data)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse_lazy('users:users_logout'))
        self.assertEqual(response.status_code, 302)

        login_data = {'username': 'TeSt_uSEr@example.com',
                      'password': 'Pass123456'
                      }
        response = self.client.post(reverse_lazy('users:users_login'), login_data)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse_lazy('users:users_logout'))
        self.assertEqual(response.status_code, 302)

        login_data = {'username': 'TeSt_uSEr@example.com',
                      'password': 'Pass12345'
                      }
        response = self.client.post(reverse_lazy('users:users_login'), login_data)
        self.assertContains(response, "Please enter a correct email address and password. "
                                      "Note that both fields may be case-sensitive.")

    def test_logout(self):
        """Проверка url выхода пользователя"""
        response = self.client.post(reverse_lazy('users:users_logout'))
        self.assertEqual(response.status_code, 302)
