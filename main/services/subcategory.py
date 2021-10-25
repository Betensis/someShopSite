from typing import Optional

from django.db import models
from django.db.models import QuerySet

from main.models import MainCategory, Subcategory, Product
from main.services.base import BaseModelService


class SubcategoryService(BaseModelService):
    model = Subcategory

    @classmethod
    def get_subcategories_by_main_category(
        cls, main_category: MainCategory
    ) -> QuerySet[Subcategory]:
        return cls.filter(main_category=main_category)

    @classmethod
    def get_products_by_subcategory(cls, subcategory: Subcategory) -> Optional[QuerySet[Product]]:
        subcategory = cls.get_object_or_404(
            slug=subcategory.slug
        )
        ItemClass: models.Model = subcategory.product_model.model_class()
        if ItemClass is None:
            return None
        return ItemClass.objects.all()
