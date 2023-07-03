from django.test import TestCase
from django.urls import reverse

from shops.models import Order
from users.models import CustomUser


class OrderTestCase(TestCase):
    """Тест проверки работы заказов"""

    fixtures = {"fixtures/010_auth_group.json",
                "fixtures/011_users.json",
                "fixtures/015_shops_banner.json",
                "fixtures/020_catalog_categories.json",
                "fixtures/025_products.json",
                "fixtures/026_tags.json",
                "fixtures/027_product_image.json",
                "fixtures/030_property.json",
                "fixtures/035_productproperty.json",
                "fixtures/040_shops.json",
                "fixtures/045_offers.json",
                "fixtures/050_order_status.json",
                "fixtures/055_order.json",
                "fixtures/065_order_offer.json",
                "fixtures/070_order_status_change.json"}

    def setUp(self) -> None:
        self.user = CustomUser.objects.get(pk=11)
        self.client.force_login(self.user)
    def test_history_order_view_success(self):
        """Тестирование истории заказа"""
        order = Order.objects.filter(custom_user=self.user)
        response = self.client.get(reverse("order_history"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"№{order[0].id}")
        self.assertContains(response, f"№{order[1].id}")

    def test_order_details_view_success(self):
        """Тестирование детального отображения заказа"""
        order = Order.objects.filter(custom_user=self.user)
        response = self.client.get(reverse("order_details", kwargs={"pk": order[0].id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, order[0].address)
