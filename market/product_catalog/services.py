from django.core.paginator import Paginator
from django.db.models import Q, Min
from django.shortcuts import render

from product_catalog.forms import ProductFilterForm
from products.models import Product
from site_settings.models import SiteSettings


def get_paginator(request, products, forms):
    """Представление пагинации 'Каталог продуктов' и сессия для сортировки """

    if request.GET.get('sort'):
        request.session['sorted'] = request.GET.get('sort')
        sort = request.session['sorted']
        products = sorted_products(sort, products)
    else:
        if 'sorted' in request.session:
            sort_session = request.session['sorted']
            products = sorted_products(sort_session, products)
    # TODO Пагинацию изменить при необходимости (default=4 записи)
    pagination_value = SiteSettings.objects.values_list('pagination_size', flat=True).first()
    paginator = Paginator(products, pagination_value)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    context = {'page_obj': page_obj,
               'form': forms
               }
    return context


def sorted_products(sort, product):
    """Сортировка по критериям"""
    if sort in ('offers__price', '-offers__date_of_creation'):
        product = {products: price for products in product.order_by(sort)
                   for price in products.offers.aggregate(item=Min('price' if sort == 'offers__price'
                                                                   else 'date_of_creation'))}
        product = list(product.keys())
        return product
    elif sort in ('sorting.get_count_history()', 'sorting.get_count_reviews()'):
        product = {sorting: sorting.get_count_reviews() if sort == 'sorting.get_count_reviews()'
                   else sorting.get_count_history() for sorting in product}
        product = sorted(product.items(), key=lambda key: key[1])[::-1]
        product = [value for value, key in product]
        return product
    else:
        return product


def filter_search(session, products):
    """Фильтрация продуктов"""
    prices = session['price'].split(';')
    sessions = {value: key for value, key in session.items() if (session[value] and value != 'price')}
    product_search = products.filter((Q(name__icontains='' if sessions.get('name') is None else sessions['name']) &
                                      Q(offers__price__range=(prices[0], prices[1]))))

    if sessions.get('in_stock'):
        product_search = products.filter((Q(name__icontains='' if sessions.get('name') is None else sessions['name']) &
                                          Q(offers__price__range=(prices[0], prices[1]))) &
                                         Q(offers__product_in_stock=None if sessions.get('in_stock') is None else
                                         sessions['in_stock']))

    if sessions.get('free_delivery'):
        product_search = products.filter((Q(name__icontains='' if sessions.get('name') is None else sessions['name']) &
                                          Q(offers__price__range=(prices[0], prices[1]))) &
                                         Q(offers__free_shipping=None if sessions.get('free_delivery') is None else
                                         sessions['free_delivery']))
    if sessions.get('in_stock') and sessions.get('free_delivery'):
        product_search = products.filter((Q(name__icontains='' if sessions.get('name') is None else sessions['name']) &
                                          Q(offers__price__range=(prices[0], prices[1]))) &
                                         Q(offers__free_shipping=None if sessions.get('free_delivery') is None else
                                         sessions['free_delivery']) &
                                         Q(offers__product_in_stock=None if sessions.get('in_stock') is None else
                                         sessions['in_stock']))
    return product_search.distinct()


class MixinGetPost:
    """Представление 'Каталог продуктов' """

    def get(self, request):
        if 'filter' in request.session:
            sessions = request.session['filter']
            prices = sessions['price'].split(';')
            products = Product.objects.all()
            form = ProductFilterForm(request.session['filter'])
            if form.is_valid():
                form.fields['price'].widget.attrs.update({'data-from': prices[0], 'data-to': prices[1]})
                products = filter_search(sessions, products)
        else:
            form = ProductFilterForm()
            products = Product.objects.all()
        context = get_paginator(request, products, form)
        return render(request, 'product_catalog/catalog.jinja2', context=context)

    def post(self, request):
        product = Product.objects.all()
        form = ProductFilterForm(request.POST)
        if form.is_valid():
            prices = form.cleaned_data['price'].split(';')
            form.fields['price'].widget.attrs.update({'data-from': prices[0],
                                                      'data-to': prices[1]})
            # TODO Время жизни сессии можно изменить при необходимости (default=3 мин.)
            request.session.set_expiry(180)
            request.session['filter'] = form.cleaned_data
            session = request.session['filter']
            product = filter_search(session, product)
        else:
            form = ProductFilterForm()
        context = get_paginator(request, product, form)
        return render(request, 'product_catalog/catalog.jinja2', context=context)
