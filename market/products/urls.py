from django.urls import path
from .views import ProductView, ReviewsAPI

app_name = "products"

urlpatterns = [
    path("api/reviews/", ReviewsAPI.as_view(), name="review_api"),
    path("product/<int:product_id>/", ProductView.as_view(), name="product_detail"),
]
