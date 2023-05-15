from django.contrib import admin  # noqa F401

from .models import Product, ProductProperty, Property, ProductImage


class ProductPropertyInline(admin.TabularInline):
    model = Product.property.through


class ProductProductImageInline(admin.TabularInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductProductImageInline,
        ProductPropertyInline,
    ]
    list_display = 'name', 'preview'


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = 'name',


@admin.register(ProductProperty)
class ProductProperty(admin.ModelAdmin):
    list_display = 'product', 'property', 'value',
