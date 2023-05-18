from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core import validators
from .models import PhoneNumberValidator, validate_image_size, phone_unique_validator


def email_unique_validator(value):
    """Проверка уникальности адреса электронной почты"""
    if User.objects.select_related('profile').filter(email=value).exists():
        raise ValidationError('Email %s уже используется другим пользователем.' % value)


class RegisterForm(UserCreationForm):

    """Форма для регистрации пользователя"""

    avatar = forms.ImageField(required=False,
                              label='Фото профиля',
                              validators=[validators.validate_image_file_extension,
                                          validate_image_size
                                          ]
                              )
    phone_number = forms.CharField(max_length=20,
                                   min_length=8,
                                   required=True,
                                   label='Телефон',
                                   validators=[PhoneNumberValidator,
                                               phone_unique_validator
                                               ],
                                   help_text='Номер телефона должен начинаться с "+" и  содержать только цифры'
                                   )
    first_name = forms.CharField(max_length=30, required=True, label='Имя')
    last_name = forms.CharField(max_length=30, required=True, label='Фамилия')
    email = forms.EmailField(required=True, validators=[email_unique_validator], label='Email')

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
