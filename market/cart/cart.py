import datetime
import json

from django.conf import settings
from .models import Cart as CartModel, CartItem
from shops.models import Offer
from django.core.exceptions import ObjectDoesNotExist


class Cart(object):

    def __init__(self, request):
        # initialization customer cart
        self.session = request.session
        self.user = request.user
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            print('no cart')
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        cart = self.cart_to_json(self.cart)
        for item in cart:
            yield item

    def cart_to_json(self, cart):
        cart_json = []
        if self.user_db_cart(cart):
            try:
                cart_items = CartItem.objects.filter(cart=cart)
                for item in cart_items:
                    cart_json.append({
                        'offer': item.offer,
                        'quantity': item.quantity,
                        'created_at': item.created_at,
                    })
            except ObjectDoesNotExist:
                cart_json = []
        else:
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

    @staticmethod
    def user_db_cart(cart):
        return True if isinstance(cart, CartModel) else False

    def add_to_cart(self, offer: Offer, quantity):
        offer_id = str(offer.id)
        if offer_id in self.cart:
            print(type(quantity))
            self.cart[offer_id]['quantity'] += int(quantity)
            print(type(self.cart[offer_id]['quantity']))
            print(self.cart[offer_id]['quantity'])
        else:
            self.cart[offer.id] = {'quantity': int(quantity), 'created_at': json.dumps(datetime.datetime.now(), default=str)}
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
        print(self.cart)

    def cart_quantity_change(self, offer: Offer, quantity):
       pass
