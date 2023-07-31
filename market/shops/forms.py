from django import forms


class OderLoginUserForm(forms.Form):
    """Форма для логирования пользователя"""

    email = forms.EmailField(widget=forms.EmailInput)
    password = forms.CharField(
        widget=forms.PasswordInput,
        max_length=100,
    )
