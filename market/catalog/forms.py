from django import forms
from django.utils.translation import gettext_lazy as _

from catalog.price_and_discounts import max_price, min_price, check_discount_price


class ProductFilterForm(forms.Form):
    """Форма заполнения фильтров"""
    check_discount_price()

    price = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "range-line",
                "type": "text",
                "data-type": "double",
                "data-min": str(min_price()),
                "data-max": str(max_price()),
                "data-from": str(min_price() + (min_price() * 30/100)),
                "data-to": str(max_price() - (max_price() * 20/100)),
            }
        ),
    )
    name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": _("Название")}),
    )
    in_stock = forms.BooleanField(required=False)
    free_delivery = forms.BooleanField(required=False)
