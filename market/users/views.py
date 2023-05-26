from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.contrib.auth.views import LoginView, LogoutView, FormView
from django.views.generic import CreateView
from .forms import CustomUserCreationForm, CustomAuthenticationForm, RestorePasswordForm
from .models import CustomUser


class UserRegistrationView(CreateView):
    """ Регистрация нового пользователя """

    form_class = CustomUserCreationForm
    model = CustomUser
    template_name = 'users_register.jinja2'
    success_url = '/'


class MyLoginView(LoginView):
    """Вход пользователя"""
    LoginView.next_page = reverse_lazy('users:users_register')
    redirect_authenticated_user = True
    template_name = 'user_login.jinja2'
    authentication_form = CustomAuthenticationForm


class UserLogoutView(LogoutView):
    """Выход пользователя"""
    next_page = reverse_lazy("users:users_login")


class RestorePasswordView(FormView):
    """Восстановление пароля пользователя"""
    form_class = RestorePasswordForm
    template_name = 'user_restore_password.jinja2'
    success_url = reverse_lazy('users:users_restore_password')

    def form_valid(self, form):
        """Проверка валидности формы"""
        super().form_valid(form)
        user_email = form.cleaned_data['email']
        new_password = CustomUser.objects.make_random_password()
        current_user = CustomUser.objects.filter(email__exact=user_email).first()
        current_user.set_password(new_password)
        current_user.save()
        send_mail(subject='Password reset instructions',
                  message=f'New password: {new_password}',
                  from_email='admin@gmail.com',
                  recipient_list=[form.cleaned_data['email']])
        success_message = f'Новый пароль успешно отправлен на {user_email} '
        return redirect(reverse_lazy('users:users_restore_password') + '?success_message=' + success_message)
