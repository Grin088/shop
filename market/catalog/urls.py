from django.urls import path

from catalog.views import show_catalog

urlpatterns = [
    path('', show_catalog, name='show_catalog')
]
