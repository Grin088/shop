from django import forms
from django.contrib.auth.forms import BaseUserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import CustomUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate


def emai_existed_validator(value):
    """Проверка существования пользователя по email """
    if not CustomUser.objects.filter(email__exact=value).first():
        raise ValidationError(f'Пользователя {value} не существует.')


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

    class Meta:
        model = CustomUser
        fields = 'email', 'username'


class CustomAuthenticationForm(AuthenticationForm):
    """ Форма для входа пользователя"""

    def clean(self):
        """Перевод имени пользователя в нижний регистр """
        username = self.cleaned_data.get("username")
        username = username.lower()
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()

            self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class RestorePasswordForm(forms.Form):
    """ Форма восстановления пароля"""

    email = LowerEmailField(required=True,
                            validators=[emai_existed_validator],
                            help_text=_('Укажите email пользователя'),
                            )
