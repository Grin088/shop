from django.shortcuts import render  # noqa F401
from django.views.generic import DetailView

from products.models import Product


class ProductDetailView(DetailView):
    model = Product
    template_name = 'market/products/product_detail.jinja2'
    context_object_name = 'product_detail'
