from django.core.paginator import Paginator
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


def filter_search(request, products):
    sessions = request.session['filter']
    prices = sessions['price'].split(';')
    # {'price': '33641;58295', 'name': '', 'in_stock': True, 'free_delivery': False}
    if sessions['name']:
        product_search = products.filter(name__icontains=sessions['name'], offers__price__range=(prices[0], prices[1]))
    else:
        product_search = products.filter(offers__price__range=(prices[0], prices[1]))
    if sessions['name'] and sessions['in_stock']:
        product_search = products.filter(name__icontains=sessions['name'], offers__price__range=(prices[0], prices[1]))

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
                products = filter_search(request, products)
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
            product = filter_search(request, product)
        else:
            form = ProductFilterForm()
        context = get_paginator(request, product, form)
        return render(request, 'product_catalog/catalog.jinja2', context=context)
