from main.models import MainCategory
from main.services.base import BaseService
from . import subcategory as subcategory_service


class MainCategoryService(BaseService):
    model = MainCategory

    @classmethod
    def get_items_by_main_category(cls, main_category: MainCategory):
        subcategory = (
            subcategory_service.SubcategoryService.get_subcategories_by_main_category(
                main_category
            ).first()
        )
        item_model = subcategory.item_model.model_class()
        return item_model.objects.all()
