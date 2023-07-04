from products.models import Browsing_history
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from django.contrib.auth.views import LoginView, LogoutView, FormView
from django.contrib.auth import update_session_auth_hash, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.views.generic.edit import FormMixin
from django.views.generic.base import View
from .forms import (CustomUserCreationForm,
                    CustomAuthenticationForm,
                    RestorePasswordForm,
                    UserProfileForm,
                    ChangePasswordForm,
                    )
from .models import CustomUser
from users.services.users import last_order_request


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
        context = {'username': name,
                   'user': user,
                   'order': last_order_request(request.user)}
        return render(request, 'market/users/account.jinja2', context)


class MyProfileView(LoginRequiredMixin, FormMixin, View):
    form_class = ChangePasswordForm
    second_form_class = UserProfileForm
    template_name = 'market/users/profile.jinja2'
    success_url = reverse_lazy('users:users_profile')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get(self, request, *args, **kwargs):
        second_form = self.second_form_class(instance=request.user)
        user = CustomUser.objects.get(pk=request.user.pk)
        form = self.get_form()
        return render(request, self.template_name, {'form': form,
                                                    'second_form': second_form,
                                                    'user': user})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        second_form = self.second_form_class(instance=request.user, data=request.POST, files=request.FILES)

        if form.is_valid() and second_form.is_valid():
            return self.form_valid(form, second_form)
        else:
            return self.get(request, *args, **kwargs)

    def form_valid(self, form, second_form):
        if form.cleaned_data.get('new_password1') and form.cleaned_data.get('new_password2'):
            form.save()
            # Обновление сведений об аутентификации пользователя
            update_session_auth_hash(self.request, form.user)
            # Автоматический вход пользователя после изменения пароля
            login(self.request, form.user)
        second_form.save()
        success_message = 'Профиль успешно сохранен'
        return redirect(reverse('users:users_profile') + '?success_message=' + success_message)


class BrowsingHistory(View):
    def get(self, request):
        """В будущем добавить фильтр для пользователя"""
        history = Browsing_history.objects.all().order_by('-data_at')[:20]
        history_count = Browsing_history.objects.count()
        contex = {
            'count': history_count,
            'history': history
        }
        return render(request, 'browsing_history.jinja2', context=contex)

    def post(self, request):
        product_id = self.request.POST.get('delete')
        history = Browsing_history.objects.all().order_by('-data_at')[:20]
        if 'delete' in request.POST:
            Browsing_history.objects.filter(product_id=product_id).delete()
        history_count = Browsing_history.objects.count()
        contex = {
            'count': history_count,
            'history': history
        }
        return render(request, 'browsing_history.jinja2', context=contex)
