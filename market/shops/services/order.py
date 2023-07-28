from unicodedata import decimal

from shops.models import OrderOffer
from site_settings.models import SiteSettings


# TODO добавить из настроек 200 и 2000
def pryce_delivery(cart: int, total_cost: decimal) -> decimal:
    """ Расчет стоимости доставки """

    list_shops = OrderOffer.objects.values_list("offer__shop_id", flat=True).distinct().filter(
        order=cart)  # TODO Заменить на смеж тб. корзины и order на cart.
    delivery = SiteSettings.objects.values_list('standard_shipping_price', flat=True).first()
    min_order_amount_free_shipping = SiteSettings.objects.values_list('free_shipping_min_order_amount', flat=True).first()
    if total_cost > int(min_order_amount_free_shipping) and len(list_shops) == 1:
        delivery = 0
    return delivery
