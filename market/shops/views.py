from django.shortcuts import render  # noqa F401
from .models import Banner
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from .models import Sellers


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


def seller_detail(request, seller_id):
    """Детальная страница продавца"""
    seller = Sellers.objects.get(id=seller_id)
    context = {
        'seller': seller,
    }
    return render(request, 'seller_detail.jinja2', context)  # пока не сделал шаблон
