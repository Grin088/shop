from django import forms


class ProductFilterForm(forms.Form):
    price = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': "range-line", 'type': "text",
                                                                         'data-type': "double", 'data-min': "2000",
                                                                         'data-max': "100000", 'data-from': "5000",
                                                                         'data-to': "30000"}))
    name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': "Название"}))
    in_stock = forms.BooleanField(required=False, label='Товары только в наличии')
    free_delivery = forms.BooleanField(required=False, label='Бесплатная доставка')
