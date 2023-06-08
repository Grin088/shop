from django.shortcuts import render, redirect  # noqa F401
from django.views.generic import TemplateView
from rest_framework.views import APIView
from django.http import JsonResponse
from products.models import Review
from .forms import ReviewFrom
from .services.product_services import ProductsServices


class ReviewsAPI(APIView):
    """Класс для отправки данных об отзывах через API"""

    def get(self, request):
        """Создание JSON для модели Review"""
        product_id = request.GET.get("product_id")
        offset = int(request.GET.get("offset", 0))
        limit = int(request.GET.get("limit", 3))
        reviews = Review.get_review(product_id=product_id)[offset: offset + limit]
        data = [
            {
                "number": n + 1,
                "user": {
                    "id": r.user.id,
                    "username": r.user.username,
                    "firstname": r.user.first_name,
                    "lastname": r.user.last_name,
                    "avatar": r.user.avatar.url,
                },
                "product": r.product.name,
                "rating": r.rating,
                "text": r.review_text,
                "created": r.created_at,
            }
            for n, r in enumerate(reviews)
        ]
        return JsonResponse({"data": data})


class ProductView(TemplateView):
    """Класс для отображения деталей продукта"""

    template_name = "market/products/product_detail.jinja2"
    form_class = ReviewFrom

    def get_context_data(self, **kwargs):
        """Получение необходимого контекста"""
        services = ProductsServices(
            request=self.request, product_id=self.kwargs.get("product_id")
        )
        context = super().get_context_data(**kwargs)
        context.update(services.get_context(form=self.form_class()))
        return context


class BaseView(TemplateView):
    template_name = 'market/base.jinja2'
