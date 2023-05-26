from django.shortcuts import render
from django.views import View
from django_jinja.views.generic import ListView

from products.models import Product


class ViewShows(ListView):
    template_name = 'product_catalog/catalog.jinja2'
    model = Product
    context_object_name = 'products'
