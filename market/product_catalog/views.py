from django.shortcuts import render, get_object_or_404
from django.views import View


from products.models import Product
from shops.models import Offer, Shop


class ViewShows(View):
    def get(self, request):
        shops = len(Offer.objects.all())
        context = {
            'offers': Offer.objects.all(),
            'shops': shops
        }
        return render(request, 'product_catalog/catalog.jinja2', context=context)


class ProductDetailView(View):
    def get(self, request, pk: int):
        product = get_object_or_404(Offer, pk=pk)
        context = {
            'offer': product
        }
        return render(request, 'product_catalog/product_detail.jinja2', context=context)
