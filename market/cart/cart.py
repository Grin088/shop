import datetime
import json

from django.conf import settings
from .models import Cart as CartModel, CartItem
from shops.models import Offer
from django.core.exceptions import ObjectDoesNotExist
from .forms import CartQuantity


class Cart(object):

    def __init__(self, request):
        # initialization customer cart
        self.session = request.session
        self.user = request.user
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        cart = self.cart_to_json(self.cart)
        for item in cart:
            yield item

    @staticmethod
    def cart_to_json(cart):
        cart_json = []
        for key, value in cart.items():
            try:
                offer = Offer.objects.get(id=key)
                cart_json.append({
                    'offer': offer,
                    'quantity': cart[key]['quantity'],
                    'created_at': cart[key]['created_at'],
                })
            except ObjectDoesNotExist:
                cart_json = []
        return cart_json

    def save_to_db(self, session_cart):
        pass

    def add_to_cart(self, offer: Offer, quantity):
        offer_id = str(offer.id)
        if offer_id in self.cart:
            self.cart_quantity_change(offer, quantity)
        else:
            self.cart[offer.id] = {'quantity': int(quantity), 'created_at': json.dumps(datetime.datetime.now(), default=str)}
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def cart_quantity_change(self, offer: Offer, quantity):
        offer_id = str(offer.id)
        self.cart[offer_id]['quantity'] += int(quantity)
