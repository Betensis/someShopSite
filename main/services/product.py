from itertools import zip_longest
from typing import Optional

from django.db.models import QuerySet, Model

from main.models import Product, MainCategory, Subcategory, Brand
from main.utils.commons import remove_none
from main.utils.product import get_product_sub_models, is_valid_sex_name


class ProductService:
    def __init__(self, prepare_query: bool = True):
        self.__products = self.__get_prepared_products() if prepare_query else None

    @staticmethod
    def __get_prepared_products() -> list[QuerySet[Product]]:
        products_models = get_product_sub_models().values()
        products = list(map(lambda x: x.objects.all(), products_models))

        return products

    def __filter_products(self, *args, **kwargs) -> "ProductService":
        self.__products = map(
            lambda product_query: product_query.filter(*args, **kwargs), self.__products
        )

        return self

    def for_kids(self, is_product_for_kids: bool) -> "ProductService":
        return self.__filter_products(for_kids=is_product_for_kids)

    def sex(self, sex_name: Product.SexChoice) -> "ProductService":
        return self.__filter_products(sex=sex_name)

    def main_category(self, main_category: MainCategory) -> "ProductService":
        return self.__filter_products(category__main_category=main_category)

    def subcategory(self, subcategory: Subcategory) -> "ProductService":
        return self.__filter_products(category=subcategory)

    def brand(self, brand: Brand) -> "ProductService":
        return self.__filter_products(brand=brand)

    def get_products(self) -> list:
        return remove_none(
            [
                product
                for product_tuple in zip_longest(*self.__products)
                for product in product_tuple
            ]
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
