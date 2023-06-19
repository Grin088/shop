from django.core.paginator import Paginator
from django.shortcuts import render
from shops.models import Offer


def get_paginator(request, products):
    paginator = Paginator(products, 4)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    context = {'page_obj': page_obj}
    return context


class MixinGetPost:

    def get(self, request):
        if 'search_filter' in request.session:
            sessions = request.session['search_filter']
            if sessions['title'] != ['']:
                product = Offer.objects.filter(price__range=(sessions['price'][0],
                                                             sessions['price'][1]),
                                               product__name__icontains=sessions['title']).order_by('price')
            else:
                if 'sort_price' in request.GET:
                    product = Offer.objects.filter(price__range=(sessions['price'][0],
                                                                 sessions['price'][1])).order_by('price')
                else:
                    product = Offer.objects.filter(price__range=(sessions['price'][0],
                                                                 sessions['price'][1]))
            context = get_paginator(request, product)
            return render(request, 'product_catalog/catalog.jinja2', context=context)
        else:
            product = Offer.objects.all()
            context = get_paginator(request, product)
        return render(request, 'product_catalog/catalog.jinja2', context=context)

    def post(self, request):
        product = Offer.objects.all()
        if 'filter' in request.POST:
            q = request.POST
            price = q.get('price').split(';')
            title = q.getlist('title')
            for name in title:
                if name != '':
                    title = name
            in_stock = q.getlist('in_stock')
            free_delivery = q.getlist('free_delivery')
            request.session['search_filter'] = {'price': price,
                                                'title': title,
                                                'in_stock': in_stock,
                                                'free_delivery': free_delivery}
            if title != ['']:
                product = Offer.objects.filter(product__name__icontains=title,
                                               price__range=(price[0],
                                                             price[1]))
            else:
                product = Offer.objects.filter(price__range=(price[0],
                                                             price[1]))
            context = get_paginator(request, product)
            return render(request, 'product_catalog/catalog.jinja2', context=context)

        context = get_paginator(request, product)
        return render(request, 'product_catalog/catalog.jinja2', context=context)
