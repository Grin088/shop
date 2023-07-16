from ..models import Banner
from site_settings.models import SiteSettings


def banner():
    """Функция для главной страницы для вывода трёх случайных активных баннеров.
     Баннеры закешированы на десять минут"""
    banners_count = SiteSettings.objects.values_list('banners_count', flat=True).first()
    random_banners = Banner.objects.filter(active=True).order_by('?')[:banners_count]
    return random_banners
