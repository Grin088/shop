from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile
from django.contrib.auth.models import User
# from django.contrib.auth.forms import BaseUserCreationForm
# from django import forms


# class CustomUserCreationForm(BaseUserCreationForm):
#     email = forms.EmailField(required=True)
#
#
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
#
#
# @admin.register(CustomUser)
# class CustomUserAdmin(UserAdmin):
#
#     inlines = [
#         ProfileInline
#     ]
#
#     add_form = CustomUserCreationForm
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'email', 'password1', 'password2'),
#         }),
#     )
#     list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')


admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    inlines = [
        ProfileInline
    ]
