from django.contrib.auth import user_logged_in
from django.dispatch import receiver
from cart.cart import Cart


@receiver(user_logged_in)
def after_user_logged_in(request, sender, user, **kwargs):
    cart = Cart(request)
    cart.save_to_db()
