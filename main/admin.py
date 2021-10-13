from django.contrib import admin

from .models import MainCategory, Subcategory, Shoes


@admin.register(MainCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "main_category"]


@admin.register(Shoes)
class ShoesAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "price", "category", "main_category"]

    @admin.display(description="Основная категория")
    def main_category(self, obj):
        return obj.category.main_category
