from collections import Counter
from django.contrib import messages
from django.contrib import admin  # noqa F401
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import Shop, Offer, Banner, Order, OrderStatus, OrderStatusChange


class ShopProductInline(admin.TabularInline):
    model = Shop.products.through


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    inlines = [
        ShopProductInline,
    ]
    list_display = (
        "name",
        "user",
        "phone_number",
        "email",
    )

    def save_formset(self, request, form, formset, change):
        products = list()
        instances = formset.save(commit=False)
        for list_products in instances:
            products.append(list_products.product.name)
            list_products.save()
        b = Counter(products)
        print(products)
        for name, count in b.items():
            if count > 1:
                # raise ValidationError(f'Вы выбрали одинаковый продукт: {name}')
                return messages.error(request, f'Ошибка. Вы выбрали 2 одинаковых продукта: {name}')
            else:
                formset.save_m2m()


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = (
        "shop",
        "product",
        "price",
    )


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    """вывод и фильтрация полей баннера в административной панели"""

    list_display = ("title", "description", "image", "active")
    list_filter = ("active",)
    search_fields = ("title",)


class OrderOfferAdminInline(admin.TabularInline):
    """Вставка модели Order"""

    model = Order.offer.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Отображение заказов в интерфейсе администратора"""

    inlines = [
        OrderOfferAdminInline,
    ]
    list_display = (
        "id",
        "custom_user",
        "status",
        "data",
        "delivery",
        "citi",
        "address",
    )


@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    """Отображение статусов заказав в интерфейсе администратора"""

    list_display = (
        "sort_index",
        "name",
    )


@admin.register(OrderStatusChange)
class OrderStatusChangeAdmin(admin.ModelAdmin):
    """Отображение истории изменения статусов заказав в интерфейсе администратора"""

    list_display = (
        "id",
        "time",
        "src_status_id",
        "dst_status_id",
    )
