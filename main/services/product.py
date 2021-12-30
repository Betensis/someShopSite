from itertools import zip_longest
from typing import Optional, Type, Any, Generator

from django.db.models import QuerySet, Model

from main.models import Product, MainCategory, Subcategory, Brand
from main.utils.service.product import get_product_sub_models, is_valid_sex_name
from main.utils.shared import remove_none


class ProductService:
    def __init__(self):
        self.__filter_options_dict = {}

    @staticmethod
    def __get_product_models() -> list[Type[Product]]:
        return list(get_product_sub_models().values())

    def __set_filter_options(self, **kwargs):
        self.__filter_options_dict.update(kwargs)

    def __filter_products(self, **kwargs) -> "ProductService":
        self.__set_filter_options(**kwargs)

        return self

    def for_kids(self, is_product_for_kids: bool) -> "ProductService":
        return self.__filter_products(for_kids=is_product_for_kids)

    def sex(self, sex_name: Product.SexChoice) -> "ProductService":
        return self.__filter_products(sex=sex_name, sex__isnull=True)

    def main_category(self, main_category: MainCategory) -> "ProductService":
        return self.__filter_products(category__main_category=main_category)

    def subcategory(self, subcategory: Subcategory) -> "ProductService":
        return self.__filter_products(category=subcategory)

    def brand(self, brand: Brand) -> "ProductService":
        return self.__filter_products(brand=brand)

    def get_products(self) -> Generator[Any, Any, None]:
        product_models = self.__get_product_models()
        if self.__filter_options_dict == {}:
            products = map(
                lambda product_model: product_model.objects.all(), product_models
            )
        else:
            products = map(
                lambda product_model: product_model.objects.filter(
                    **self.__filter_options_dict
                ),
                product_models,
            )

        return remove_none(
            (
                product
                for product_tuple in zip_longest(*products)
                for product in product_tuple
            )
        )

    @classmethod
    def get_products_by_subcategory(
        cls, subcategory_slug: str, sex: str = None
    ) -> Optional[QuerySet[Product]]:
        subcategory = Subcategory.objects.get_or_none(slug=subcategory_slug)
        if subcategory is None:
            return None

        ItemClass: Model = subcategory.product_content_type.model_class()
        if ItemClass is None:
            return None

        if sex is not None and not is_valid_sex_name(sex):
            return None
        if sex is None:
            return ItemClass.objects.all()
        return ItemClass.objects.filter(sex=sex)
