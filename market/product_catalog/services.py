from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

from product_catalog.forms import ProductFilterForm
from products.models import Product


def get_paginator(request, products, forms):
    paginator = Paginator(products, 4)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    context = {'page_obj': page_obj,
               'form': forms
               }
    return context


def filter_search(session, products):
    prices = session['price'].split(';')
    sessions = {value: key for value, key in session.items() if (session[value] and value != 'price')}
    product_search = products.filter((Q(name__icontains='' if sessions.get('name') is None else sessions['name']) &
                                      Q(offers__price__range=(prices[0], prices[1])))).distinct()

    if sessions.get('in_stock'):
        product_search = products.filter((Q(name__icontains='' if sessions.get('name') is None else sessions['name']) &
                                          Q(offers__price__range=(prices[0], prices[1]))) &
                                         Q(offers__product_in_stock=None if sessions.get('in_stock') is None else
                                         sessions['in_stock'])).distinct()

    if sessions.get('free_delivery'):
        product_search = products.filter((Q(name__icontains='' if sessions.get('name') is None else sessions['name']) &
                                          Q(offers__price__range=(prices[0], prices[1]))) &
                                         Q(offers__free_shipping=None if sessions.get('free_delivery') is None else
                                         sessions['free_delivery'])).distinct()
    if sessions.get('in_stock') and sessions.get('free_delivery'):
        product_search = products.filter((Q(name__icontains='' if sessions.get('name') is None else sessions['name']) &
                                          Q(offers__price__range=(prices[0], prices[1]))) &
                                         Q(offers__free_shipping=None if sessions.get('free_delivery') is None else
                                         sessions['free_delivery']) &
                                         Q(offers__free_shipping=None if sessions.get('free_delivery') is None else
                                         sessions['free_delivery'])).distinct()
    return product_search


class MixinGetPost:
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
            products = Product.objects.all().distinct()
        context = get_paginator(request, products, form)
        return render(request, 'product_catalog/catalog.jinja2', context=context)

    def post(self, request):
        product = Product.objects.all()
        form = ProductFilterForm(request.POST)
        if form.is_valid():
            prices = form.cleaned_data['price'].split(';')
            form.fields['price'].widget.attrs.update({'data-from': prices[0],
                                                      'data-to': prices[1]})
            request.session.set_expiry(180)
            request.session['filter'] = form.cleaned_data
            session = request.session['filter']
            product = filter_search(session, product)
        else:
            form = ProductFilterForm()
        context = get_paginator(request, product, form)
        return render(request, 'product_catalog/catalog.jinja2', context=context)
