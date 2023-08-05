from django.shortcuts import redirect
from django.urls import reverse

from catalog.models import Catalog


def get_categories(request):
    search = request.GET.get('query')
    catalog = Catalog.objects.all()
    list_catalog = list()
    list_catalog_parent = list()
    for cat in catalog:
        if cat.parent:
            list_catalog_parent.append(cat.parent)
        else:
            list_catalog.append(cat)
    if search:
        request.session.set_expiry(180)
        request.session['search'] = search
    return {'list_category': list_catalog,
            'list_category_parent': list_catalog_parent,
            'categories': catalog}
