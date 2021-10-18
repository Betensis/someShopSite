from django.contrib import admin

from .models import MainCategory, Subcategory, Shoes, Brand, Hat, OrderItem, Order


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


@admin.register(Shoes, Hat)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": ("title",),
    }
    list_display = [
        "title",
        "description",
        "price",
        "category",
        "get_main_category",
        "brand",
        "slug",
    ]

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


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        "customer",
        "ordered",
        "content_type",
        "object_id",
        "content_object",
    ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "customer",
        "get_items",
        "ordered_date",
        "ordered",
    ]

    @admin.display(description="items")
    def get_items(self, obj):
        return ", ".join(
            [
                f"{item.get_content_type_repr()} id:{item.object_id}"
                for item in obj.items.all()
            ]
        )
