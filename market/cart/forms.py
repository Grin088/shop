from django import forms


class CartQuantity(forms.Form):
    quantity = forms.IntegerField()
