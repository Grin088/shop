from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from discounts.models import ShopItemDiscount, CartItemDiscount


class ShopDiscountCreationForm(forms.ModelForm):
    """Форма для создания записи в таблице скидок для магазина"""

    class Meta:
        model = ShopItemDiscount
        fields = "__all__"

    def clean(self):
        """Функция проверки введенных данных"""
        cleaned_data = super().clean()

        # проверка, хотя бы одно из полей условия заполнено.
        if ("products" and "categories") in cleaned_data:
            if not (cleaned_data.get("products") or cleaned_data.get("categories")):
                self.add_error(
                    None, _("Заполните хотя бы одно поле для категории или товаров")
                )

        discount_amount = cleaned_data.get("discount_amount")
        discount_amount_type = cleaned_data.get("discount_amount_type")
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        # Проверка даты и установка новой в случае выполнения условия.
        if start_date < timezone.now():
            cleaned_data["start_date"] = timezone.now()
        # Проверка разности дат начала и окончания действия скидки
        if start_date > end_date:
            self.add_error(
                "end_date",
                _(
                    "Дата окончания действия скидки должна быть больше даты начала действия скидки"
                ),
            )
        # Проверка значения скидки в %.
        if discount_amount_type == 1 and discount_amount > 99:
            self.add_error("discount_amount", _("Скидка в % не должна превышать 99 %"))
        return cleaned_data


class CartDiscountCreationForm(ShopDiscountCreationForm):
    """Форма для создания записи в таблице скидок для корзины"""

    min_total_price_of_cart = forms.DecimalField(
        min_value=0,
        max_digits=10,
        decimal_places=2,
        label=_("Минимальная цена товаров в корзине"),
        help_text=_("Скидка может быть установлена на стоимость товаров в корзине."),
        required=False
    )
    max_total_price_of_cart = forms.DecimalField(
        min_value=0,
        max_digits=10,
        decimal_places=2,
        label=_("Максимальная цена товаров в корзине"),
        required=False
    )

    class Meta:
        model = CartItemDiscount
        fields = "__all__"

    def clean(self):
        """Функция проверки введенных данных"""
        cleaned_data = super().clean()
        products_group_1 = cleaned_data.get("products_group_1")
        products_group_2 = cleaned_data.get("products_group_2")
        min_total_price_of_cart = cleaned_data.get("min_total_price_of_cart")
        max_total_price_of_cart = cleaned_data.get("max_total_price_of_cart")
        min_amount_product_in_cart = cleaned_data.get("min_amount_product_in_cart")
        max_amount_product_in_cart = cleaned_data.get("max_amount_product_in_cart")

        # Проверка, что выбраны товары из второй группы, если выбраны товары из первой группы.
        if products_group_1 and not products_group_2:
            self.add_error("products_group_2", _("Выберете товары для второй группы"))
        # Проверка, товар из 2 группы не содержаться в 1.
        if products_group_1 and products_group_2:
            for product in products_group_1:
                if products_group_2.filter(pk=product.pk):
                    self.add_error(
                        "products_group_2",
                        _(f"Товар: '{product.name}' уже указан в 1 группе.")
                    )
                    break
        # Проверка, минимальная цена меньше максимальной.
        if min_total_price_of_cart and max_total_price_of_cart:
            if min_total_price_of_cart > max_total_price_of_cart:
                self.add_error(
                    "max_total_price_of_cart",
                    _("Максимальная сумма должна быть больше минимальной"),
                )
        # Минимальное количество продуктов в корзине меньше максимального.
        if min_amount_product_in_cart and max_amount_product_in_cart:
            if min_amount_product_in_cart > max_amount_product_in_cart:
                self.add_error(
                    "max_amount_product_in_cart",
                    _(
                        "Максимальное количество товаров в корзине должно быть больше минимального"
                    ),
                )
        # Проверка, заполнение хотя бы одного из полей условия для получения скидки.
        if not (
            products_group_1
            or products_group_2
            or min_total_price_of_cart
            or max_total_price_of_cart
            or min_amount_product_in_cart
            or max_amount_product_in_cart
        ):
            self.add_error(
                None, _("Заполните хотя бы одно условие для получения скидки")
            )
        return cleaned_data
