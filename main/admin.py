from django.contrib import admin

from .models import MainCategory, Subcategory, Shoes, Brand, Hat


@admin.register(MainCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ["title"]


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "main_category"]


@admin.register(Shoes, Hat)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "description",
        "price",
        "category",
        "get_main_category",
        "brand",
    ]

    @admin.display(description="Основная категория")
    def get_main_category(self, obj):
        return obj.category.main_category


@admin.register(Brand)
class Brand(admin.ModelAdmin):
    list_display = ["title"]
