from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from users.models import User


class UserProfileTest(TestCase):
    """Создание профиля"""

    @classmethod
    def setUpClass(cls):
        """Создание пользователя"""
        super().setUpClass()
        cls.user = User.objects.create_user(username='a', email='AAAAAAAAA@adadafa.com', password="123")
        cls.user2 = User.objects.create_superuser(username='b', email='AAAAA@adadafa.Ru', password="123")

    #
    # @classmethod
    # def tearDownClass(cls):
    #     """ Удаление пользователя"""
    #     super().tearDownClass()
    #     cls.user.delete()

    def test_data_profile(self):
        """Проверка данных профиля созданного пользователя"""

        self.client.login(username='Test_user', password="123")
        print('hello worls')
        print(self.user.username)
        print(self.user.email)
        print(self.user.is_superuser)
        print(self.user2.is_superuser)
        # avatar = self.user.profile.avatar
        # phone = self.user.profile.phone_number
        # self.assertEqual(avatar, "users/avatars/default/default_avatar1.png")
        # self.assertEqual(phone, '+0000000000')


# class RegistrationFormTest(TestCase):
#     """ Проверка страницы регистрации и входа """
#
#     def setUp(self):
#         self.user = User.objects.create_user(username='Admin12', password='Pass123456')
#         self.url = reverse_lazy('users:users_register')
#         self.data1 = {
#             'username': 'test_user',
#             'first_name': 'Test',
#             'last_name': 'User',
#             'email': 'test_user@example.com',
#             'password1': 'Pass123456',
#             'password2': 'Pass123456',
#             'phone_number': '+1234567890'
#         }
#
#         self.data2 = {
#             'username': 'test_user1',
#             'first_name': 'Test1',
#             'last_name': 'User1',
#             'email': 'Test_user@example.com',
#             'password1': 'Pass123456',
#             'password2': 'Pass123456',
#             'phone_number': '+1234567890'
#         }
#
#     def test_registration_form(self):
#         """Проверка формы регистрации"""
#         response = self.client.post(self.url, data=self.data1)
#         self.assertEqual(response.status_code, 302)
#         user = User.objects.get(username=self.data1['username'])
#         self.assertEqual(user.first_name, self.data1['first_name'])
#         self.assertEqual(user.last_name, self.data1['last_name'])
#         self.assertEqual(user.email, self.data1['email'])
#         self.assertEqual(user.profile.phone_number, self.data1['phone_number'])
#         self.assertEqual(user.profile.avatar, "users/avatars/default/default_avatar1.png")
#
#         response = self.client.post(self.url, data=self.data2)
#         self.assertContains(response, 'Email test_user@example.com уже используется другим пользователем.')
#         self.assertContains(response, 'Пользователь с номером +1234567890 уже существует.')
#
#     def test_login(self):
#         """Проверка входа """
#         login_data = {'username': 'Admin12',
#                       'password': 'Pass123456'
#                       }
#         response = self.client.post(reverse_lazy('users:users_login'), login_data)
#
#         self.assertEqual(response.status_code, 302)
#         login_data2 = {'username': 'Admin12',
#                        'password': 'Pass12345'
#                        }
#
#         response = self.client.get(reverse_lazy('users:users_logout'))
#         response = self.client.post(reverse_lazy('users:users_login'), login_data2)
#         self.assertContains(response, 'Please enter a correct username and password. '
#                                       'Note that both fields may be case-sensitive.')
#
#     def test_logout(self):
#         """Проверка url выхода пользователя"""
#         response = self.client.post(reverse_lazy('users:users_logout'))
#         self.assertEqual(response.status_code, 302)
