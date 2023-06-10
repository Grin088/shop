from django.urls import path
from .views import ProductView, ReviewsAPI
from django.conf import settings  # noqa F401
from django.views.decorators.cache import cache_page  # noqa F401

app_name = "products"

urlpatterns = [
    path("api/reviews/", ReviewsAPI.as_view(), name="review_api"),
    path("product/<int:product_id>/",
         # cache_page(settings.CACHE_CONSTANT)(ProductView.as_view()),
         ProductView.as_view(),
         name="product_detail"),
]

# TODO реализация сброса кэша после обновления товара
