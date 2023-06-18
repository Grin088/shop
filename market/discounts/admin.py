from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from discounts.models import ShopItemDiscount, CartItemDiscount
from discounts.forms import ShopDiscountCreationForm, CartDiscountCreationForm


@admin.register(ShopItemDiscount)
class ShopDiscountAdmin(admin.ModelAdmin):
    """Класс для отображения скидок на товары в магазине"""

    form = ShopDiscountCreationForm
    list_display = ("name", "active", "formatted_last_time")
    search_fields = ["name"]

    def formatted_last_time(self, obj):
        """Функция для отображения окончания действия скидки"""
        last_time = obj.last_discount_time
        # Если срок действия скидки <= 0, выводится значение "
        if not last_time:
            obj.active = False
            obj.save()
            return mark_safe(
                f'<span style="color: red;">{_("Время действия скидки истекло !")}</span>'
            )
        return last_time

    formatted_last_time.short_description = _("Время до окончания действия скидки")


@admin.register(CartItemDiscount)
class CartDiscountAdmin(admin.ModelAdmin):
    """Класс для отображения скидок на товары в корзине"""

    form = CartDiscountCreationForm
    list_display = ("name", "active", "formatted_last_time")
    search_fields = ["name"]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "description",
                    "discount_amount",
                    "discount_amount_type",
                    "active",
                    "start_date",
                    "end_date",
                )
            },
        ),
        (
            _("Скидка на группу товаров"),
            {"fields": ("products_group_1", "products_group_2")},
        ),
        (
            _("Дополнительные параметры"),
            {
                "fields": (
                    "min_total_price_of_cart",
                    "max_total_price_of_cart",
                    "min_amount_product_in_cart",
                    "max_amount_product_in_cart",
                )
            },
        ),
    )

    def formatted_last_time(self, obj):
        """Функция для отображения окончания действия скидки"""
        last_time = obj.last_discount_time
        # Если срок действия скидки <= 0, выводится значение "
        if not last_time:
            obj.active = False
            obj.save()
            return mark_safe(
                f'<span style="color: red;">{_("Время действия скидки истекло !")}</span>'
            )
        return last_time

    formatted_last_time.short_description = _("Время до окончания действия скидки")
