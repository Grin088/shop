from django.urls import path

from product_catalog.views import ViewShows, ProductDetailView

urlpatterns = [
    path('', ViewShows.as_view(), name='show_product'),
    # path('detail/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),

]
