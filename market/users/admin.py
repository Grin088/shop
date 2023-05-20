from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.auth.forms import BaseUserCreationForm, UserChangeForm
from django import forms
from .models import Profile, EmailUniqueValidator



class CustomUserCreationForm(BaseUserCreationForm):
    """Форма для создания нового пользователя"""
    email_unique_validator = EmailUniqueValidator()
    email = forms.EmailField(required=True, validators=[email_unique_validator])


class CustomUserChangeForm(UserChangeForm):
    """ Форма обновления данных пользователя"""
    email_unique_validator = EmailUniqueValidator()
    email = forms.EmailField(required=True, validators=[email_unique_validator])


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    inlines = [
        ProfileInline
    ]
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )
