from decimal import Decimal
from typing import Any
from django.db.models import F, Sum
from django.db import transaction

from cart.models import CartItem
from shops.models import OrderOffer, OrderStatusChange, OrderStatus, Order


def pryce_delivery(r_user: Any) -> (dict):
    """ Расчет стоимости доставки """
    cart_list = CartItem.objects.filter(cart__user=r_user). \
        annotate(summ_offer=F('offer__price') * F('quantity')).select_related("offer__product", "offer__shop")

    min_price_offer = Decimal(2000.00)
    delivery_express = Decimal(500.00)
    delivery_ordinary = Decimal(200.00)
    cart_count_shop = cart_list.all().values_list("offer__shop").distinct().count()
    total_cost = cart_list.all().aggregate(summ=Sum("summ_offer"))["summ"]

    if total_cost > min_price_offer and cart_count_shop == 1:
        delivery_ordinary = Decimal(0.00)
    total_cost_delivery_ordinary = total_cost + delivery_ordinary
    total_cost_delivery_express = total_cost + delivery_express
    return {"total_cost_ordinary": total_cost_delivery_ordinary,
            "total_cost_express": total_cost_delivery_express,
            "delivery_express": delivery_express,
            "delivery_ordinary": delivery_ordinary,
            }


@transaction.atomic
def save_order_model(r_user: Any, r_post: Any) -> None:
    """
    Сохранение заказа и истории изменения статуса
    """
    cart_list = CartItem.objects.filter(cart__user=r_user). \
        annotate(summ_offer=F('offer__price') * F('quantity')).select_related("offer__product")

    if r_post.get('delivery') == "ORDINARY":
        total_cost = pryce_delivery(r_user)["total_cost_ordinary"]
    else:
        total_cost = pryce_delivery(r_user)["total_cost_express"]

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
    order_status.dst_status = OrderStatus.objects.get(sort_index=5)
    order_status.save()

    return new_order.pk