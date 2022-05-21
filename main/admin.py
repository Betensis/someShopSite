from django.contrib import admin

from .models import (
    MainCategory,
    Category,
    Brand,
    Product,
    ProductInfoTags,
    ProductWarehouseInfo,
)


@admin.register(MainCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = [
        "title",
        "slug",
    ]


@admin.register(Category)
class SubcategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = [
        "title",
        "main_category",
        "slug",
    ]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = [
        "title",
        "slug",
    ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "title",
        "price",
        "category",
        "brand",
        "sex",
        "last_update",
        "get_info_tags",
    ]

    @admin.display(description="info tags", empty_value="--empty--")
    def get_info_tags(self, product):
        represented_tags = ", ".join(
            map(lambda tag: tag.title, product.info_tags.all())
        )

        return represented_tags or None


@admin.register(ProductInfoTags)
class ProductInfoTagAdmin(admin.ModelAdmin):
    list_display = [
        "title",
    ]


@admin.register(ProductWarehouseInfo)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ["product", "product_size", "product_quantity"]
