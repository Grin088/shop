from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _


class Discount(models.Model):
    """Абстрактны класс для создания моделей скидок"""

    class Meta:
        abstract = True

    DISCOUNT_AMOUNT_TYPE_CHOICES = (
        (1, _("проценты")),
        (2, _("сумма")),
    )

    name = models.CharField(
        max_length=50, null=False, blank=False, verbose_name=_("название скидки")
    )
    description = models.TextField(max_length=150, verbose_name=_("Описание скидки"))
    discount_amount = models.PositiveIntegerField(
        verbose_name=_("размер скидки"), null=False, blank=False
    )
    discount_amount_type = models.PositiveSmallIntegerField(
        choices=DISCOUNT_AMOUNT_TYPE_CHOICES, null=False, blank=False
    )
    active = models.BooleanField(
        verbose_name=_("Скидка активна"), null=False, blank=False
    )
    start_date = models.DateTimeField(
        null=False, blank=False, verbose_name=_("дата начала действия скидки")
    )
    end_date = models.DateTimeField(
        null=False, blank=False, verbose_name=_("дата окончания действия скидки")
    )

    def __str__(self):
        return f"id: {self.id} name: {self.name}"

    @property
    def last_discount_time(self):
        """Получение оставшегося времени действия скидки"""
        if self.active:
            current_time = timezone.now()
            last_time = self.end_date - current_time
            return last_time if last_time.total_seconds() >= 0 else False
        return self.active


class ShopItemDiscount(Discount):
    """Модель скидок для товаров в магазине"""

    class Meta:
        verbose_name = _("скидка на товар в магазине")
        verbose_name_plural = _("скидки на товары в магазине")

    products = models.ManyToManyField(
        "products.Product",
        blank=True,
        related_name="shop_items_discounts",
        verbose_name=_("товары"),
    )
    categories = models.ManyToManyField(
        "catalog.Catalog",
        blank=True,
        related_name="shop_items_discounts",
        verbose_name=_("категории товаров"),
    )


class CartItemDiscount(Discount):
    """Модель скидок для товаров в корзине"""

    class Meta:
        verbose_name = _("скидка на товар в корзине")
        verbose_name_plural = _("скидки на товары в корзине")

    products_group_1 = models.ManyToManyField(
        "products.Product",
        blank=True,
        related_name="cart_item_discounts_group_1",
        verbose_name=_("группа товаров 1"),
        help_text=_(
            "Скидка может быть установлена на группу товаров, если они вместе находятся в корзине."
            " Указывается группа товаров 1 и группа товаров 2."
        ),
    )

    products_group_2 = models.ManyToManyField(
        "products.Product",
        blank=True,
        related_name="cart_item_discounts_group_2",
        verbose_name=_("группа товаров 2"),
    )

    min_total_price_of_cart = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Минимальная цена товаров в корзине"),
        help_text=_("Скидка может быть установлена на стоимость товаров в корзине."),
    )
    max_total_price_of_cart = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Максимальная цена товаров в корзине"),
    )

    min_amount_product_in_cart = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Минимальное количество товаров в корзине"),
        help_text=_("Скидка может быть установлена на количество товаров в корзине."),
    )
    max_amount_product_in_cart = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Максимальное количество товаров в корзине"),
    )

    def __str__(self):
        return f"id: {self.id} name: {self.name}"
