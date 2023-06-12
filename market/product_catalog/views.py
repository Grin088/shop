from django.shortcuts import render, get_object_or_404
from django.views import View
from shops.models import Offer
from product_catalog import services


class ViewShows(services.MixinGetPost, View):
    pass


class ProductDetailView(View):
    def get(self, request, pk: int):
        product = get_object_or_404(Offer, pk=pk)
        context = {
            'offer': product
        }
        return render(request, 'product_catalog/product_detail.jinja2', context=context)
