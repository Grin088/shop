from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import BaseUserCreationForm
from django.core import validators
from django.core.exceptions import ValidationError
from .models import PhoneNumberValidator, ValidateImageSize


# def unique_phone_number(value):
#     """Проверка уникальности номера телефона"""
#     if User.objects.filter(profile__phone_number=value):
#         raise ValidationError(f'Пользователь с номером {value} уже существует.')
#
#
def emai_existed_validator(value):
    """Проверка существования пользователя по email """
    if not User.objects.filter(email__exact=value).first():
        raise ValidationError(f'Пользователя с email {value} не существует.')


class LowerEmailField(forms.EmailField):
    """ Запись email в нижнем регистре"""
    def to_python(self, value):
        value = super().to_python(value)
        if value is not None:
            value = value.lower()
        return value


class CustomUserCreationForm(BaseUserCreationForm):
    """Форма для создания нового пользователя"""
    email = forms.EmailField(required=True)


class RestorePasswordForm(forms.Form):
    """ Форма восстановления пароля"""

    email = LowerEmailField(required=True,
                            validators=[emai_existed_validator],
                            help_text='Укажите email пользователя',
                            )
