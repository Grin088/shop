from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView, FormView
from django.views.generic import CreateView
from django.contrib.auth import authenticate, login
from .forms import RegisterForm, RestorePasswordForm


class UserRegistrationView(CreateView):
    """ Регистрация нового пользователя """

    form_class = RegisterForm
    queryset = User.objects.select_related('profile')
    template_name = 'users_register.jinja2'
    success_url = '/'

    def form_valid(self, form):
        """Проверка валидности формы"""
        response = super().form_valid(form)
        avatar = form.cleaned_data.get('avatar')
        self.object.profile.phone_number = form.cleaned_data.get('phone_number')
        if avatar:
            self.object.profile.avatar = avatar
        self.object.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(self.request, user)
        return response


class MyLoginView(LoginView):
    """Вход пользователя"""
    LoginView.next_page = reverse_lazy('users:users_register')
    redirect_authenticated_user = True
    template_name = 'user_login.jinja2'


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
        new_password = User.objects.make_random_password()
        current_user = User.objects.filter(email__exact=user_email).first()
        current_user.set_password(new_password)
        current_user.save()
        send_mail(subject='Password reset instructions',
                  message=f'New password: {new_password}',
                  from_email='admin@gmail.com',
                  recipient_list=[form.cleaned_data['email']])
        success_message = f'Новый пароль успешно отправлен на {user_email} '
        return redirect(reverse_lazy('users:users_restore_password') + '?success_message=' + success_message)
