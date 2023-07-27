from unicodedata import decimal

from shops.models import OrderOffer


# TODO добавить из настроек 200 и 2000
def pryce_delivery(cart: int, total_cost: decimal) -> decimal:
    """Расчет стоимости доставки"""

    list_shops = (
        OrderOffer.objects.values_list("offer__shop_id", flat=True)
        .distinct()
        .filter(order=cart)
    )  # TODO Заменить на смеж тб. корзины и order на cart.
    delivery = 200
    if total_cost > 2000 and len(list_shops) == 1:
        delivery = 0
    return delivery
