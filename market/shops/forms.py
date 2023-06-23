from django.forms import ModelForm

from shops.models import Order
from users.models import CustomUser
from django.contrib.auth.forms import BaseUserCreationForm


class OderLoginUserForm(BaseUserCreationForm):
    """Форма для создания нового пользователя"""

    class Meta:
        model = CustomUser
        fields = ['email', 'password',]

class OrderForm(ModelForm):
    class Meta:
        Model = Order
        fields = ['delivery', 'citi', 'address',]






# from myauth.models import Profile
#
# class PayBalanceForm(ModelForm):
#     class Meta:
#         model = Profile
#         fields = ["balance"]
#
#
#
# from django import forms
# from django.contrib.auth.models import Group
# from django.core import validators
# from django.forms import ModelForm
#
# from .models import Product, Order, Basket
#
# class GroupForm(ModelForm):
#     class Meta:
#         model = Group
#         fields = ["name"]
#
# class ProductForms(forms.ModelForm):
#     class Meta: #1029
#         model = Product
#         fields = "name", "price", "description", "discount", "preview"
#
#     #  Расширение формы для загрузки нескольких изображений
#     images = forms.ImageField(
#         widget=forms.ClearableFileInput(attrs={"multiple": True}),
#     )
#
#
#
# class OrderForms(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = "user", "delivery_address", "promocode", "products"
#
#
#
#
#
# # class ProductForms(forms.Form):  # 1019
# #     name = forms.CharField(max_length=100)
# #     price = forms.DecimalField(min_value=1, max_value=1000000, decimal_places=2)
# #     description = forms.CharField(
# #         label="Product description",
# #         widget=forms.Textarea(attrs={"rows": 5, "cols": "30"}), #1022
# #         validators=[validators.RegexValidator(   #1021
# #             regex=r"great",
# #             message="Field must contain word 'great'"  #  Собщение если не правельный ввод даных в форму
# #         )],
# #     )
#
# class BasketForms(forms.ModelForm):
#     class Meta:
#         model = Basket
#         fields = "articles",
#
#
# class SalesReportForms(forms.Form):
#     first_date = forms.DateField(widget=forms.SelectDateWidget())
#     end_date = forms.DateField(widget=forms.SelectDateWidget())
#
#
