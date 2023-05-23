from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.auth.forms import BaseUserCreationForm, UserChangeForm
# from .models import Profile, EmailUniqueValidator
# from .forms import LowerEmailField
from .models import User, BasedAccountManager
from django import forms
from django.utils.translation import gettext_lazy as _


class AccountCreationForm(BaseUserCreationForm):
    """Форма для создания нового пользователя"""
    email = forms.EmailField(required=True)

#
#
# class CustomUserChangeForm(UserChangeForm):
#     """ Форма обновления данных пользователя"""
#     email_unique_validator = EmailUniqueValidator()
#     email = LowerEmailField(required=True, validators=[email_unique_validator])
#
#
# class ProfileInline(admin.StackedInline):
#     model = Profile
#     can_delete = False
#
#
# admin.site.register(Account)

@admin.register(User)
class AccountAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "avatar", "phone_number")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_form = AccountCreationForm
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2"),
            },
        ),
    )
