from django.shortcuts import render

from catalog.models import MPTTCatalog


def show_catalog(request):
    return render(request, 'catalog.html', {'catalog': MPTTCatalog.objects.all()})
