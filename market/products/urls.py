from django.urls import path
from . import views
from .views import ProductReviewsView, ReviewsAPI, AuthorView

app_name = "products"

urlpatterns = [
    path("api/reviews/", ReviewsAPI.as_view(), name="review_api"),
    path("review/<int:product_id>/", ProductReviewsView.as_view(), name="product_review"),
    path("a", AuthorView.as_view(), name="pr_review"),
]
