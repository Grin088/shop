from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from .forms import RegisterForm, RestorePasswordForm
from django.contrib.auth import authenticate
from django.contrib.auth import login


def register_view(request):
    """ Регистрация нового пользователя """
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            avatar = form.cleaned_data.get('avatar')
            user = form.save()
            user.profile.phone_number = form.cleaned_data.get('phone_number')
            if avatar:
                user.profile.avatar = avatar
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'users_register.jinja', {'form': form})


class MyLoginView(LoginView):
    """Вход пользователя"""
    LoginView.next_page = reverse_lazy('users:users_register')
    redirect_authenticated_user = True
    template_name = 'user_login.jinja'


class UserLogoutView(LogoutView):
    """Выход пользователя"""
    next_page = reverse_lazy("users:users_login")


def restore_password_view(request):
    """ Восстановление пароля"""
    if request.method == 'POST':
        form = RestorePasswordForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            new_password = User.objects.make_random_password()
            current_user = User.objects.filter(email=user_email).first()
            if current_user:
                current_user.set_password(new_password)
                current_user.save()
                send_mail(subject='Восстановление пароля',
                          message=f'Новый пароль: {new_password}',
                          from_email='admin@gmail.com',
                          recipient_list=[form.cleaned_data['email']])
                return HttpResponse('Письмо с новым паролем было успешно отправлено')

    restore_password_form = RestorePasswordForm()
    context = {
        'form': restore_password_form
    }
    return render(request, 'user_restore_password.jinja', context=context)
