from django.contrib import admin  # noqa F401

from .models import Shop, Offer, Banner


class ShopProductInline(admin.TabularInline):
    model = Shop.products.through


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    inlines = [
        ShopProductInline,
    ]
    list_display = 'name',


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = 'shop', 'product', 'price',


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'image', 'active')
    list_filter = ('active',)
    search_fields = ('title',)

