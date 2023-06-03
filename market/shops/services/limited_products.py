import random
from datetime import timedelta
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from products.models import Product
from ..tasks import update_product_of_the_day


def get_random_limited_edition_product():
    """Получает список всех товаров с флагом limited_edition"""
    products = Product.objects.filter(limited_edition=True)
    if products:
        product = random.choice(products)
        return product
    else:
        return None


def time_left():  # пока не может использоваться из-за celery
    limited_products = cache.get('limited_products')
    if not limited_products:
        update_product_of_the_day.delay()
        limited_products = Product.objects.none()

    time_left = (cache.ttl('limited_products') or 0) - 86000  # 23 часа + отклонения
    time_left = max(time_left, 0)  # Удаляем отрицательное значение
    time_left = timedelta(seconds=time_left)

    return {
        'limited_products': limited_products,
        'time_left': time_left,
    }


def get_offer_of_the_day_cache_key():
    """ Получает уникальный ключ для кеширования предложения дня"""
    key = make_template_fragment_key('offer_of_the_day')
    return key


def invalidate_offer_of_the_day_cache():
    """ Сбрасывает кеш предложения дня"""
    key = get_offer_of_the_day_cache_key()
    cache.delete(key)