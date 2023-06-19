from django import forms


class ProductFilterForm(forms.Form):
    # ordering = forms.ChoiceField(label='Сортировка', required=False, choices=[
    #     ['price', 'По популярности #В разработке#'],
    #     ['price', 'Сначала дешевые'],
    #     ['-price', 'Сначала дорогие'],
    #     ['price', 'По отзывам #В разработке#'],
    #     ['price', 'По новизне #В разработке#']
    # ])
    # min_price = forms.IntegerField(label='от', required=False)
    # max_price = forms.IntegerField(label='до', required=False)
    pass
