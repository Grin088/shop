import random
from datetime import datetime, time, timedelta
from celery import shared_task
from django.core.cache import cache
from products.models import Product


@shared_task
def update_product_of_the_day(name="Task time left"):
    """таск для обновления времени каждые 24 часа и выбор рандомного продукта из ограниченного тиража"""
    now = datetime.now()
    midnight = datetime.combine(now.date(), time.min)
    time_left = (midnight + timedelta(days=1) - now).seconds
    products = Product.objects.filter(limited_edition=True)
    product = random.choice(products)
    cache.set('limited_products', product, time_left)
