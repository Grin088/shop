from django.shortcuts import render  # noqa F401
from .models import Banner
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy

from .models import Shop
from .services import is_member_of_group


@cache_page(settings.CACHE_CONSTANT)
def home(request):
    """Функция для главной страницы для вывода трёх случайных активных баннеров.
     Баннеры закешированы на десять минут"""
    random_banners = Banner.objects.filter(active=True).order_by('?')[:3]

    context = {
        'random_banners': random_banners,
    }
    return render(request, 'market/base.jinja2', context)


class BaseView(TemplateView):
    template_name = 'market/base.jinja2'


@user_passes_test(
    is_member_of_group('Sellers'),
    login_url=reverse_lazy('account')
)
def seller_detail(request):
    """Детальная страница продавца"""
    if request.method == 'GET':
        shop = Shop.objects.filter(user=request.user.id)
        context = {
            'shop': shop,
        }
        return render(request, 'seller_detail.jinja2', context)
