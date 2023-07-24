from decimal import Decimal

from shops.models import OrderOffer


# TODO добавить из настроек 200 и 2000
def pryce_delivery(count_offer: int, total_cost: Decimal) -> (dict):
    """ Расчет стоимости доставки """
    delivery_express = Decimal(500.00)
    delivery_ordinary = Decimal(200.00)

    if total_cost > 2000 and count_offer == 1:
        delivery_ordinary = Decimal(0.00)
    total_cost_delivery_ordinary = total_cost + delivery_ordinary
    total_cost_delivery_express = total_cost + delivery_express
    return {"total_cost_ordinary": total_cost_delivery_ordinary,
            "total_cost_express": total_cost_delivery_express,
            "delivery_express": delivery_express,
            "delivery_ordinary": delivery_ordinary,
            }
