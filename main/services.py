from django.db.models import QuerySet

from .models import Subcategory, MainCategory


def get_subcategories_by_main_category(main_category: MainCategory) -> QuerySet[Subcategory]:
    return Subcategory.objects.filter(main_category=main_category)


def get_items_by_main_category(main_category: MainCategory):
    subcategory = get_subcategories_by_main_category(main_category).first()
    item_model = subcategory.item_model.model_class()
    return item_model.objects.all()
