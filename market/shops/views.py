from django.shortcuts import render  # noqa F401
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView, View
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin

from users.views import MyLoginView
from shops.forms import OderLoginUserForm
from shops.services import banner
from shops.services.catalog import get_featured_categories
from shops.services.compare import (compare_list_check,
                                    splitting_into_groups_by_category,
                                    get_comparison_lists_and_properties,
                                    )
from shops.services.limited_products import get_random_limited_edition_product, get_top_products, get_limited_edition
# from .services.limited_products import time_left  # пока не может использоваться из-за celery
from shops.models import Shop, Order, OrderOffer
from shops.services.is_member_of_group import is_member_of_group


@cache_page(settings.CACHE_CONSTANT)
def home(request):
    if request.method == "GET":
        featured_categories = get_featured_categories()
        random_banners = banner.banner()
        top_products = get_top_products()
        # time_and_products = time_left()  # пока не может использоваться из-за celery
        # update_time = time_and_products['time_left']  # пока не может использоваться из-за celery
        # limited_products = time_and_products['limited_products']  # пока не может использоваться из-за celery
        limited_product = get_random_limited_edition_product()
        limited_edition = get_limited_edition().exclude(id=limited_product.id)[:16]
        context = {
            'featured_categories': featured_categories,
            'random_banners': random_banners,
            # 'update_time': update_time,  # пока не может использоваться из-за celery
            'limited_product': limited_product,
            'top_products': top_products,
            'limited_edition': limited_edition,
        }
        return render(request, 'market/index.jinja2', context=context)


class BaseView(TemplateView):
    template_name = 'market/base.jinja2'


@user_passes_test(
    is_member_of_group('Sellers'),
    login_url=reverse_lazy('account')
)
def seller_detail(request):
    """Детальная страница продавца"""
    if request.method == 'GET':
        shop = Shop.objects.filter(user=request.user.id)
        context = {
            'shop': shop,
        }
        return render(request, 'seller_detail.jinja2', context)


class ComparePageView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        """Страница сравнения"""
        # TODO Добавляет список  для отработки сравнения
        # compare_list_check(request.session, 4)
        comp_list = request.session.get("comp_list", [])

        if comp_list and len(comp_list) > 1:
            category_offer_dict = splitting_into_groups_by_category(comp_list)
            list_compare, list_property = get_comparison_lists_and_properties(list(category_offer_dict.values())[0])
            context = {
                "category_offer_dict": sorted([(name, len(count)) for name, count in category_offer_dict.items()],
                                              key=lambda x: x[1], reverse=True),
                "list_compare": list_compare,
                "list_property": list_property
            }
            return render(request, "shops/comparison.jinja2", context=context)

        return render(request, "shops/comparison.jinja2", context={"text": "Не достаточно данных для сравнения."})

    def post(self, request: HttpRequest) -> HttpResponse:
        """Переключение категории сравнения и удаление из списка сравнений"""

        delete_id = request.POST.get('delete_id')
        if delete_id:
            compare_list_check(request.session, int(delete_id))

        comp_list = request.session.get("comp_list", [])
        if len(comp_list) > 1:
            category_name = request.POST.get("category")
            category_offer_dict = splitting_into_groups_by_category(comp_list)
            list_compare, list_property = get_comparison_lists_and_properties(category_offer_dict[category_name])

            context = {"category_offer_dict": sorted([(name, len(count))
                                                      for name, count in category_offer_dict.items()],
                                                     key=lambda x: x[1], reverse=True),
                       "list_compare": list_compare,
                       "list_property": list_property,
                       }
            return render(request, 'shops/comparison.jinja2', context=context)

        return render(request, "shops/comparison.jinja2", context={"text": "Не достаточно данных для сравнения."})


class OrderView(TemplateView):
    """Оформление заказа"""

    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "user": request.user,
            "form": OderLoginUserForm
        }
        return render(request, "order/order.jinja2", context=context)

    def post(self, request: HttpRequest) -> HttpResponse:

        if not request.user.is_authenticated:
            user = authenticate(email=request.POST.get("email"), password=request.POST.get("password"))

            if user:
                login(request, user)
            else:
                return render(request, "order/order.jinja2", context={"text": "Неправильный ввод эмейла или пароля",
                                                                      "user": request.user,
                                                                      })

        # delivery = request.POST.get("delivery")
        # city = request.POST.get("city")
        # address = request.POST.get("address")
        # pay = request.POST.get("pay") # TODO online and someone

        context = {
            "user": request.user,
        }
        return render(request, "order/order.jinja2", context=context)


class OrderLoginView(MyLoginView):
    """Вход пользователя"""
    next_page = reverse_lazy('order')


class HistoryOrderView(LoginRequiredMixin, View):
    """История заказов"""
    login_url = reverse_lazy("users:users_login")

    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "orders": Order.objects.filter(custom_user_id=request.user).prefetch_related("status").order_by("-data")
        }
        return render(request, "order/historyorder.jinja2", context=context)


class OrderDetailsView(LoginRequiredMixin, View):
    """Отображение деталей заказа"""

    login_url = reverse_lazy("users:users_login")

    def get(self, reqnuest: HttpRequest, pk: int) -> HttpResponse:
        query = Order.objects.select_related("custom_user").get(id=pk)

        if reqnuest.user != query.custom_user:
            return HttpResponse("<h1>HTTP 403 Forbidden</h1>")
        context = {
            "order": query,
            "order_offers": OrderOffer.objects.filter(order_id=pk).prefetch_related("offer__product"),
        }
        return render(reqnuest, "order/oneorder.jinja2", context=context)
