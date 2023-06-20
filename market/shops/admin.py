from django.contrib import admin# noqa F401

from .models import Shop, Offer, Banner, Order, OrderStatus, OrderStatusChange


class ShopProductInline(admin.TabularInline):
    model = Shop.products.through


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    inlines = [
        ShopProductInline,
    ]
    list_display = 'name', 'user', 'phone_number', 'email',


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = 'shop', 'product', 'price',


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'image', 'active')
    list_filter = ('active',)
    search_fields = ('title',)


class OrderOfferAdminInline(admin.TabularInline):
    model = Order.offer.through



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderOfferAdminInline,
    ]
    list_display = 'id', 'custom_user', 'status', 'data',

@admin.register(OrderStatus)
class OrderAdmin(admin.ModelAdmin):
    list_display = 'sort_index', 'name'


@admin.register(OrderStatusChange)
class ShopAdmin(admin.ModelAdmin):
    list_display = 'id', 'time', 'src_status_id', 'dst_status_id'