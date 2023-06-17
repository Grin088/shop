from django.shortcuts import render, redirect  # noqa F401
from django.views.generic import TemplateView, CreateView
from rest_framework.views import APIView
from django.urls import reverse_lazy
from django.core.management import call_command
from django.http import JsonResponse
from .models import Review, Import
from .forms import ReviewFrom, ImportForm
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


class BaseView(TemplateView):
    template_name = 'market/base.jinja2'


class ImportCreateView(CreateView):
    """ представление для запуска импорта"""
    model = Import # модель для создания объекта
    form_class = ImportForm # форма для ввода данных
    template_name = 'market/products/import_form.jinja2' # шаблон для отображения формы
    success_url = reverse_lazy('import_data:import_list') # URL для перенаправления после успешного создания объекта

    def form_valid(self, form):
        # метод для обработки валидной формы

        # вызываем родительский метод для создания объекта модели Import с данными из формы
        response = super().form_valid(form)

        # получаем имя файла или URL и email из формы
        source = form.cleaned_data['source']
        email = form.cleaned_data['email']

        # вызываем команду для запуска импорта с указанными аргументами
        call_command('import_data', source, '--email', email, '--save')

        # возвращаем ответ родительского метода
        return response