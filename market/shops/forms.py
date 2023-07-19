from django.contrib.auth.forms import BaseUserCreationForm

from users.models import CustomUser


class OderLoginUserForm(BaseUserCreationForm):
    """Форма для логирования пользователя"""

    class Meta:
        model = CustomUser
        fields = ['email', 'password',]
