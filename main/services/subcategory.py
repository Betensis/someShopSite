from django.db.models import QuerySet

from main.models import MainCategory, Subcategory
from main.services.base import BaseService


class SubcategoryService(BaseService):
    model = Subcategory

    @classmethod
    def get_subcategories_by_main_category(cls, main_category: MainCategory) -> QuerySet[Subcategory]:
        return cls.filter(main_category=main_category)
