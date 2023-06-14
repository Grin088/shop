from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.contrib.auth.views import LoginView, LogoutView, FormView
from django.views import View
from django.views.generic import CreateView

from products.models import Browsing_history, Product
from .forms import CustomUserCreationForm, CustomAuthenticationForm, RestorePasswordForm
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
