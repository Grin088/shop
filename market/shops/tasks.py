import random
from datetime import datetime, time, timedelta
from celery import shared_task
from django.core.cache import cache
from products.models import Product


@shared_task
def update_product_of_the_day():
    now = datetime.now()
    midnight = datetime.combine(now.date(), time.min)
    time_left = (midnight + timedelta(days=1) - now).seconds
    products = Product.objects.filter(limited_edition=True)
    product = random.choice(products)
    cache.set('limited_products', product, time_left)
