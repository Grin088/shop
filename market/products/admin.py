from django.contrib import admin  # noqa F401

from .models import Product, ProductProperty, Property


class ProductPropertyInline(admin.TabularInline):
    model = Product.property.through


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductPropertyInline,
    ]
    list_display = 'name',


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = 'name',


@admin.register(ProductProperty)
class ProductProperty(admin.ModelAdmin):
    list_display = 'product', 'property', 'value',
