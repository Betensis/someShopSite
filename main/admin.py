from django.contrib import admin

from .models import (
    MainCategory,
    Subcategory,
    Shoes,
    Brand,
    HatDress,
    OrderProduct,
    Order,
    Outerwear,
)


@admin.register(MainCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = [
        "title",
        "slug",
    ]


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = [
        "title",
        "main_category",
        "slug",
    ]


@admin.register(Shoes, HatDress, Outerwear)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": ("title",),
    }
    list_display = [
        "title",
        "price",
        "category",
        "get_main_category",
        "brand",
        "slug",
        "sex",
        "for_kids",
    ]

    def for_kids(self, obj):
        return obj.is_for_kids

    @admin.display(description="Основная категория")
    def get_main_category(self, obj):
        return obj.category.main_category


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = [
        "title",
        "slug",
    ]


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = [
        "customer",
        "content_type",
        "object_id",
        "content_object",
        "order",
    ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "customer",
        "products",
        "ordered_date",
        "ordered",
    ]
