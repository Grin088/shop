from django.core.paginator import Paginator
from django.shortcuts import render
from products.models import Product


def get_paginator(request, products):
    paginator = Paginator(products, 4)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    context = {'page_obj': page_obj,
               }
    return context


class MixinGetPost:
    def get(self, request):
        products = Product.objects.all()
        context = get_paginator(request, products)
        return render(request, 'product_catalog/catalog.jinja2', context=context)

    def post(self, request):
        product = Product.objects.all()
        if 'filter' in request.POST:

            context = get_paginator(request, product)
            return render(request, 'product_catalog/catalog.jinja2', context=context)

        context = get_paginator(request, product)
        return render(request, 'product_catalog/catalog.jinja2', context=context)
