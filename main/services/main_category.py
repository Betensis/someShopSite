from django.db.models import QuerySet

from main.models import MainCategory
from main.services.base import BaseModelService
from . import subcategory as subcategory_service


class MainCategoryService(BaseModelService):
    model = MainCategory

    @classmethod
    def get_products_by_main_category(
        cls, main_category: MainCategory
    ) -> QuerySet[MainCategory]:
        subcategory = (
            subcategory_service.SubcategoryService.get_subcategories_by_main_category(
                main_category
            ).first()
        )
        item_model = subcategory.product_model.model_class()
        return item_model.objects.all()
