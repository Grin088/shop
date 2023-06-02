from django.urls import path
from products.views import ProductDetailView

urlpatterns = [
    path('<int:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('', ProductDetailView.as_view(), name='index'),
    path('', ProductDetailView.as_view(), name='login'),
    path('', ProductDetailView.as_view(), name='registr'),
    path('', ProductDetailView.as_view(), name='catalog'),
    path('', ProductDetailView.as_view(), name='comparison'),
    path('', ProductDetailView.as_view(), name='cart'),
    path('', ProductDetailView.as_view(), name='account'),
]
