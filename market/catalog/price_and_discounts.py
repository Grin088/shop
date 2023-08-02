from django.db.models import Min, Max, Avg

from products.models import Product


def min_price():
    products = Product.objects.all()
    check_discount_price(products)
    price = products.annotate(price_min_discount=Avg('offers__discount_price')).aggregate(Min('price_min_discount'))
    return round(price['price_min_discount__min'] or 0)


def max_price():
    products = Product.objects.all()
    check_discount_price(products)
    price = products.annotate(price_max_discount=Avg('offers__discount_price')).aggregate(Max('price_max_discount'))
    return round(price['price_max_discount__max'] or 0)


def check_discount_price(products):
    """Обновление цены со скидкой"""
    for product in products:
        for ii in product.offers.only('discount_price'):
            ii.discount_price = ii.price_with_discount
            ii.save()
