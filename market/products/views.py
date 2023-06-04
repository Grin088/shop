from django.shortcuts import render, redirect  # noqa F401
from django.views.generic import TemplateView
from rest_framework.views import APIView
from django.http import JsonResponse
from products.models import Review
from .forms import ReviewFrom
from .services.product_services import ReviewServices


class ReviewsAPI(APIView):
    """Класс для отправки данных об отзывах через API"""

    @classmethod
    def get(cls, request):
        """Создание JSON для модели Review"""
        product_id = request.GET.get("product_id")
        offset = int(request.GET.get("offset", 0))
        limit = int(request.GET.get("limit", 3))
        reviews = Review.get_review(product_id=product_id)[offset : offset + limit]
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

    template_name = "market/products/product.jinja2"
    form_class = ReviewFrom

    def get_context_data(self, **kwargs):
        """Получение необходимого контекста"""
        services = ReviewServices(
            request=self.request, product_id=self.kwargs.get("product_id")
        )
        context = super().get_context_data(**kwargs)
        context.update(services.get_context(form=self.form_class()))
        return context

    def post(self, request, product_id):
        """Обработка добавления отзыва"""
        form = self.form_class(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.user_id = request.user.id
            review.product_id = product_id
            review.save()
            return redirect("/")

        context = self.get_context_data(product_id=product_id)
        context["form"] = form
        return self.render_to_response(context)
