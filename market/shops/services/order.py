from decimal import Decimal
from typing import Any

from django.db import transaction
from django.db.models import QuerySet
from django.http import HttpRequest

from shops.models import OrderOffer, OrderStatusChange, OrderStatus, Order


# TODO добавить из настроек 200 и 2000
def pryce_delivery(cart_list: QuerySet) -> (dict):
    """ Расчет стоимости доставки """
    delivery_express = Decimal(500.00)
    delivery_ordinary = Decimal(200.00)
    cart_count_offer = len(set([x.offer_id for x in cart_list]))
    total_cost = sum([x.summ_offer for x in cart_list])

    if total_cost > 2000 and cart_count_offer == 1:
        delivery_ordinary = Decimal(0.00)
    total_cost_delivery_ordinary = total_cost + delivery_ordinary
    total_cost_delivery_express = total_cost + delivery_express
    return {"total_cost_ordinary": total_cost_delivery_ordinary,
            "total_cost_express": total_cost_delivery_express,
            "delivery_express": delivery_express,
            "delivery_ordinary": delivery_ordinary,
            }


@transaction.atomic
def save_order_model(r_user: Any, r_post: Any, cart_list: QuerySet) -> None:
    """
    Сохранение заказа и истории изменения статуса
    """
    if r_post.get('delivery') == "ORDINARY":
        total_cost = pryce_delivery(cart_list)["total_cost_ordinary"]
    else:
        total_cost = pryce_delivery(cart_list)["total_cost_express"]

    new_order = Order()
    new_order.custom_user = r_user
    new_order.status = OrderStatus.objects.get(sort_index=1)
    new_order.delivery = r_post['delivery']
    new_order.city = r_post['city']
    new_order.address = r_post['address']
    new_order.pay = r_post['pay']
    new_order.total_cost = total_cost
    new_order.save()

    for item_cart_i in cart_list:
        cart2order = OrderOffer()
        cart2order.offer = item_cart_i.offer
        cart2order.order = new_order
        cart2order.count = item_cart_i.quantity
        cart2order.price = item_cart_i.summ_offer
        cart2order.save()

    order_status = OrderStatusChange()
    order_status.order = new_order
    order_status.src_status = OrderStatus.objects.get(sort_index=1)
    order_status.dst_status = OrderStatus.objects.get(sort_index=2)
    order_status.save()