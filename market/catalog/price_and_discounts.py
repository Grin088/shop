from django.db.models import Min, Max, Avg
from products.models import Product

products = Product.objects.all()


def min_price():
    check_discount_price()
    price = Product.objects.annotate(price_min_discount=Avg('offers__discount_price'))
    price_min = price.aggregate(Min('price_min_discount'))
    return round(price_min['price_min_discount__min' or None])


def max_price():
    price = products.annotate(price_max_discount=Avg('offers__discount_price'))
    price_max = price.aggregate(Max('price_max_discount'))
    return round(price_max['price_max_discount__max' or None])


def check_discount_price():
    """Обновление цены со скидкой"""
    for product in products:
        for ii in product.offers.only('discount_price'):
            ii.discount_price = ii.price_with_discount
            ii.save()
