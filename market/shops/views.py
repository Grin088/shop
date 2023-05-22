from django.shortcuts import render  # noqa F401
from .models import Banner
from django.conf import settings
from django.views.decorators.cache import cache_page


@cache_page(settings.CACHE_CONSTANT)
def home(request):
    """Функция для главной страницы для вывода трёх случайных активных баннеров.
     Баннеры закешированы на десять минут"""
    random_banners = Banner.objects.filter(active=True).order_by('?')[:3]

    context = {
        'random_banners': random_banners,
    }
    return render(request, 'market/banner.jinja2', context)  # пока нет шаблона banner, тут будет base
