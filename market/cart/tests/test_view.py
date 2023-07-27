from django.test import TestCase

from cart.models import Cart, CartItem
from products.models import Product
from shops.models import Shop, Offer
from users.models import CustomUser


class CartViewTest(TestCase):
    """Класс тестирования элемента корзины"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = CustomUser.objects.create(username="user_test", password="123", email="testuser@gmail.com")
        cls.cart = Cart.objects.create(user=cls.user)
        cls.shop = Shop.objects.create(name="test_shop", user=cls.user)
        cls.product = Product.objects.create(name="test_product")
        cls.offer = Offer.objects.create(shop=cls.shop, product=cls.product, price=100)
        cls.cart_item = CartItem.objects.create(cart=cls.cart, offer=cls.offer, quantity=100)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        CartViewTest.cart_item.delete()
        CartViewTest.offer.delete()
        CartViewTest.product.delete()
        CartViewTest.shop.delete()
        CartViewTest.cart.delete()
        CartViewTest.user.delete()

    def test_template_cart(self):
        response = self.client.get("/cart/cart_items/", follow=True)
        self.assertEqual(response.status_code, 200)
        # TODO не могу указать путь к темплейту
        # self.assertTemplateUsed(response, 'market/cart/cart.jinja2')

    def test_details(self):
        # TODO не понимаю как в сессию положить что то
        self.client.post("/cart/add/1/0")
        session = self.client.session
        self.assertEqual(session["cart"], {})
