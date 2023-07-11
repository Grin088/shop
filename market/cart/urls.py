from django.urls import path
from .views import CartView, cart_add

app_name = "cart"

urlpatterns = [
    path("cart_items/", CartView.as_view(), name="cart_items"),
    path("add/<int:pk>/<int:silent>", cart_add, name="cart_add"),
]