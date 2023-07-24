from django import forms
from shops.models import StatusDeliveryOrder, StatusPayOrder, Order



class OderLoginUserForm(forms.Form):
    """Форма для логирования пользователя"""
    email = forms.EmailField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput, max_length=100,)


# class OderForm(forms.ModelForm):
#     """Форма для логирования пользователя"""
#     delivery = forms.ChoiceField(widget=forms.RadioSelect,
#                                  choices=StatusDeliveryOrder.choices,
#                                  initial=StatusDeliveryOrder.ordinary)
#     pay = forms.ChoiceField(widget=forms.RadioSelect,
#                             choices=StatusPayOrder.choices,
#                             initial=StatusPayOrder.online,
#                             )
#     address = forms.CharField(widget=forms.Textarea, max_length=200, required=True )
#
#     class Meta:
#         model = Order
#         fields = ["delivery", "city", "address", "pay"]
