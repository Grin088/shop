from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from django.contrib.auth.views import LoginView, LogoutView, FormView
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from .forms import CustomUserCreationForm, CustomAuthenticationForm, RestorePasswordForm, UserProfileForm
from .models import CustomUser


class UserRegistrationView(CreateView):
    """ Регистрация нового пользователя """

    form_class = CustomUserCreationForm
    model = CustomUser
    template_name = 'market/users/register.jinja2'
    success_url = '/'


class MyLoginView(LoginView):
    """Вход пользователя"""
    LoginView.next_page = reverse_lazy('users:users_register')
    redirect_authenticated_user = True
    template_name = 'market/users/login.jinja2'
    authentication_form = CustomAuthenticationForm


class UserLogoutView(LogoutView):
    """Выход пользователя"""
    next_page = reverse_lazy("users:users_login")


class RestorePasswordView(FormView):
    """Восстановление пароля пользователя"""
    form_class = RestorePasswordForm
    template_name = 'market/users/password.jinja2'
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


@login_required(login_url=reverse_lazy('users:users_login'))
def account(request):
    """Личный кабинет"""
    user_account = get_object_or_404(CustomUser, email=request.user.email)
    if user_account.email != request.user.email:
        return render(request, 'market/base.jinja2')
    if request.method == 'GET':
        # Получение имени пользователя
        user = CustomUser.objects.get(pk=request.user.pk)
        if user.first_name and user.last_name:
            name = f"{user.first_name} {user.last_name}"
        else:
            name = user.username
        context = {'username': name, 'user': user}
        return render(request, 'market/users/account.jinja2', context)


@login_required(login_url=reverse_lazy('users:users_login'))
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            success_message = 'Профиль успешно сохранен'
            return HttpResponseRedirect(reverse('users:users_profile') + '?success_message=' + success_message)
    else:
        form = UserProfileForm(instance=request.user)
    context = {'form': form}
    return render(request, 'market/users/profile.jinja2', context)
