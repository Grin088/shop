from users.models import CustomUser
from django.contrib.auth.forms import BaseUserCreationForm


class OderLoginUserForm(BaseUserCreationForm):
    """Форма для логирования пользователя"""

    class Meta:
        model = CustomUser
        fields = ['email', 'password',]
