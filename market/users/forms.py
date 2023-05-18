import re
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core import validators


class RegisterFormValidators:
    """ Класс с проверками для форм"""

    @classmethod
    def phone_number_validator(cls, value):
        """Проверка соответствия номера телефона требуемому формату"""
        if not re.match(r'^\+\d+$', value):
            raise ValidationError('Номер телефона должен начинаться с + и содержать только цифры')

    @classmethod
    def phone_unique_validator(cls, value):
        """Проверка уникальности номера телефона """
        if User.objects.select_related('profile').filter(profile__phone_number=value).exists():
            raise ValidationError('%s уже используется другим пользователем.' % value)

    @classmethod
    def email_unique_validator(cls, value):
        """Проверка уникальности адреса электронной почты"""
        if User.objects.select_related('profile').filter(email=value).exists():
            raise ValidationError('Email %s уже используется другим пользователем.' % value)

    @classmethod
    def max_size_avatar_validator(cls, value):
        """Проверка максимального размера аватра профиля"""
        file_size = value.size
        if file_size > 2 * 1024 * 1024:  # 2MB
            raise ValidationError("Максимальный размер изображения не может превышать 2MB.")


class RegisterForm(UserCreationForm):

    """Форма для регистрации пользователя"""

    validator = RegisterFormValidators()
    avatar = forms.ImageField(required=False,
                              label='Фото профиля',
                              validators=[validators.validate_image_file_extension,
                                          validator.max_size_avatar_validator
                                          ]
                              )
    phone_number = forms.CharField(max_length=20,
                                   min_length=8,
                                   required=True,
                                   label='Телефон',
                                   validators=[validator.phone_number_validator,
                                               validator.phone_unique_validator
                                               ],
                                   help_text='Номер телефона должен начинаться с "+" и  содержать только цифры'
                                   )
    first_name = forms.CharField(max_length=30, required=True, label='Имя')
    last_name = forms.CharField(max_length=30, required=True, label='Фамилия')
    email = forms.EmailField(required=True, validators=[validator.email_unique_validator], label='Email')

    class Meta:
        model = User
        fields = ('avatar',
                  'username',
                  'first_name',
                  'last_name',
                  'password1',
                  'password2',
                  'email',
                  'phone_number'
                  )


class RestorePasswordForm(forms.Form):
    """ Форма для восстановления пароля"""

    email = forms.EmailField()
