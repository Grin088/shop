from django.test import TestCase
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from discounts.models import ShopItemDiscount, CartItemDiscount
from discounts.forms import ShopDiscountCreationForm, CartDiscountCreationForm
from products.models import Product
from catalog.models import Catalog


class DiscountCreateModel(TestCase):
    """Класс тестов для модели скидок"""

    fixtures = [
        "fixtures/010_auth_group.json",
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
    ]

    @classmethod
    def setUpClass(cls):
        """Установка необходимых значений"""
        super().setUpClass()
        cls.products = Product.objects.all()
        cls.categories = Catalog.objects.all()
        cls.date_now = timezone.now()
        cls.nex_date = cls.date_now + timezone.timedelta(days=1)
        cls.shop_discount_form = ShopDiscountCreationForm
        cls.cart_discount_form = CartDiscountCreationForm

    @classmethod
    def tearDownClass(cls):
        """Удаление установленных значений"""
        super().tearDownClass()
        cls.products.delete()
        cls.categories.delete()

    def test_create_shop_item_discount_success(self):
        """Создание записи скидки для товаров в магазине в таблицу через форму"""
        form_data = {
            "name": "test_shop_discount",
            "description": "some description",
            "discount_amount": 99,
            "discount_amount_type": 1,
            "start_date": self.date_now,
            "end_date": self.nex_date,
            "active": True,
        }

        categories = [self.categories.first()]
        products = [self.products.first()]
        form_data["products"] = products
        form_data["categories"] = categories
        form = self.shop_discount_form(form_data)

        if form.is_valid():
            discount = form.save(commit=False)
            discount.save()
            discount.products.set(products)
            discount.categories.set(categories)
            self.assertTrue(discount in ShopItemDiscount.objects.all())

    def test_create_cart_item_discount_success(self):
        """Создание записи скидки для товаров в корзине в таблицу через форму"""

        form_data = {
            "name": "test_shop_discount",
            "description": "some_description",
            "discount_amount": 99,
            "discount_amount_type": 1,
            "start_date": self.date_now,
            "end_date": self.nex_date,
            "active": True,
            "min_total_price_of_cart": 500,
            "max_total_price_of_cart": 1000,
            "min_amount_product_in_cart": 2,
            "max_amount_product_in_cart": 5,
        }
        products_group_1 = [self.products.first()]
        products_group_2 = [self.products.last()]

        form = self.cart_discount_form(form_data)
        if form.is_valid():
            discount = form.save(commit=False)
            discount.save()
            discount.products_group_1.set(products_group_1)
            discount.products_group_2.set(products_group_2)
            self.assertTrue(discount in CartItemDiscount.objects.all())
            self.assertEqual(discount.discount_amount, form_data["discount_amount"])

        else:
            raise ValidationError(form.errors)

    def test_create_shop_discount_failure(self):
        """Проверка вывода ошибок при создании записи скидки для товаров в магазине"""
        incorrect_form_data = {
            "name": "test_shop_discount",
            "discount_amount": 100,
            "discount_amount_type": 1,
            "start_date": self.nex_date,
            "end_date": self.date_now,
            "active": True,
        }

        form = ShopDiscountCreationForm(incorrect_form_data)
        self.assertFormError(
            form, None, _("Заполните хотя бы одно поле для категории или товаров")
        )
        self.assertFormError(
            form,
            "end_date",
            _(
                "Дата окончания действия скидки должна быть больше даты начала действия скидки"
            ),
        )
        self.assertFormError(
            form, "discount_amount", _("Скидка в % не должна превышать 99 %")
        )

    def test_create_cart_discount_with_failure(self):
        """Проверка вывода ошибок при создании записи скидки для товаров в корзине"""

        incorrect_form_data = {
            "name": "test_shop_discount",
            "discount_amount": 100,
            "discount_amount_type": 1,
            "start_date": self.nex_date,
            "end_date": self.date_now,
            "active": True,
        }

        form = self.cart_discount_form(incorrect_form_data)
        self.assertFormError(
            form, None, _("Заполните хотя бы одно условие для получения скидки")
        )
        self.assertFormError(
            form,
            "end_date",
            _(
                "Дата окончания действия скидки должна быть больше даты начала действия скидки"
            ),
        )
        self.assertFormError(
            form, "discount_amount", _("Скидка в % не должна превышать 99 %")
        )

        incorrect_form_data = {
            "name": "test_shop_discount",
            "discount_amount": 99,
            "discount_amount_type": 1,
            "start_date": self.date_now,
            "end_date": self.nex_date,
            "active": True,
            "products_group_1": [self.products.first()],
            "min_total_price_of_cart": 100,
            "max_total_price_of_cart": 50,
            "min_amount_product_in_cart": 5,
            "max_amount_product_in_cart": 2,
        }

        form = CartDiscountCreationForm(incorrect_form_data)
        self.assertFormError(
            form,
            "max_total_price_of_cart",
            _("Максимальная сумма должна быть больше минимальной"),
        )
        self.assertFormError(
            form,
            "max_amount_product_in_cart",
            _(
                "Максимальное количество товаров в корзине должно быть больше минимального"
            ),
        )
        self.assertFormError(
            form, "products_group_2", _("Выберете товары для второй группы")
        )
