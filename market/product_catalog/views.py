from django.shortcuts import render, get_object_or_404
from django.views import View

from product_catalog.forms import ProductFilterForm
from shops.models import Offer


class ViewShows(View):
    def get(self, request):
        if 'q' in request.GET:
            q = request.GET['q']
            product = Offer.objects.filter(product__name__icontains=q)
        else:
            product = Offer.objects.all()
        form = ProductFilterForm(request.GET)

        if form.is_valid():
            if form.cleaned_data['min_price']:
                product = product.filter(price__gte=form.cleaned_data['min_price'])
            if form.cleaned_data['max_price']:
                product = product.filter(price__lte=form.cleaned_data['max_price'])
            if form.cleaned_data['ordering']:
                product = product.order_by(form.cleaned_data['ordering'])
        return render(request, 'product_catalog/catalog.jinja2', {'offers': product, 'form': form})


class ProductDetailView(View):
    def get(self, request, pk: int):
        product = get_object_or_404(Offer, pk=pk)
        context = {
            'offer': product
        }
        return render(request, 'product_catalog/product_detail.jinja2', context=context)
