from django.db.models import Min, Max, Avg
from products.models import Product

products = Product.objects.all()


def min_price():
    # check_discount_price()
    price = Product.objects.annotate(price_min_discount=Avg('offers__price'))
    for i in price:
        print(i)
        print(i.price_min_discount)
    return True


def max_price():
    price = products.annotate(price_max_discount=Avg('offers__price'))
    price_max = price.aggregate(Max('price_max_discount'))
    return True


def check_discount_price():
    """Обновление цены со скидкой"""
    for product in products:
        for ii in product.offers.only('discount_price'):
            ii.discount_price = ii.price_with_discount
            ii.save()
