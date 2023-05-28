from django.shortcuts import render  # noqa F401
from .models import Banner
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView
from django.contrib.auth.decorators import user_passes_test

from .models import Shop


@cache_page(settings.CACHE_CONSTANT)
def home(request):
    """Функция для главной страницы для вывода трёх случайных активных баннеров.
     Баннеры закешированы на десять минут"""
    random_banners = Banner.objects.filter(active=True).order_by('?')[:3]

    context = {
        'random_banners': random_banners,
    }
    return render(request, 'base.html', context)  # пока нет шаблона banner, тут будет base


class BaseView(TemplateView):
    template_name = 'market/base.jinja2'


def is_seller(user):
    """Проверка на принадлежность к группе продавцов"""
    return user.groups.filter(name='Sellers').exists()


@user_passes_test(is_seller)
def seller_detail(request):
    """Детальная страница продавца"""
    if request.method == 'GET':
        shop = Shop.objects.filter(user=request.user.id)
        context = {
            'shop': shop,
        }
        return render(request, 'seller_detail.jinja2', context)


@user_passes_test(lambda u: not is_seller(u))
def user_view(request):
    pass
