from ..models import Banner


def banner():
    """Функция для главной страницы для вывода трёх случайных активных баннеров.
     Баннеры закешированы на десять минут"""
    random_banners = Banner.objects.filter(active=True).order_by('?')[:3]
    return random_banners
