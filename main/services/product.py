from django.db.models import QuerySet
from django.http import Http404
from django.shortcuts import get_object_or_404

from core import settings
from main.models import Product, MainCategory, Category, Brand
from main.utils.service.product import is_valid_sex_name, get_image_url_by_name


class ProductService:
    IMAGE_FIELD_NAME = "image"
    IMAGE_URL_FIELD_NAME = "image_url"

    def __init__(self):
        self.__filter_options_dict = {}
        self._select_related_fields = []
        self._prefetch_related_fields = []
        self._selected_fields = []

    def sex(self, sex_name: Product.SexChoice) -> "ProductService":
        if not is_valid_sex_name(sex_name):
            raise ValueError(
                f"Invalid sex name. Expected: {Product.SexChoice.values}. Now: {sex_name}"
            )
        return self.__set_filter_options(sex=sex_name, sex__isnull=True)

    def main_category(self, main_category: MainCategory) -> "ProductService":
        return self.__set_filter_options(category__main_category=main_category)

    def category(self, category: Category) -> "ProductService":
        return self.__set_filter_options(category=category)

    def brand(self, brand: Brand) -> "ProductService":
        return self.__set_filter_options(brand=brand)

    def related_field(self, *args):
        self._select_related_fields.clear()
        return self

    def prefetched_fields(self, *args):
        self._prefetch_related_fields.extend(args)
        return self

    def clear_prefetched_fields(self):
        self._prefetch_related_fields.clear()
        return self

    def selected_fields(self, *args) -> "ProductService":
        self._selected_fields.extend(args)
        return self

    def clear_selected_fields(self):
        self._selected_fields.clear()
        return self

    def get_products(self) -> QuerySet[Product]:
        products = Product.objects.filter(**self.__filter_options_dict)

        if self._prefetch_related_fields:
            products = products.prefetch_related(*self._prefetch_related_fields)
        if self._select_related_fields:
            products = products.select_related(*self._select_related_fields)
        if self._selected_fields:
            products = products.values(*self._selected_fields)

        products = self.__add_image_url_fields(products)
        return products

    def __set_filter_options(self, **kwargs) -> "ProductService":
        self.__filter_options_dict.update(kwargs)
        return self

    def __add_image_url_fields(self, products: QuerySet) -> QuerySet[Product]:
        for product in products:
            if not isinstance(product, (Product, dict)):
                raise TypeError(
                    f"Product must be instances of Product model or dict. Now: {product.__class__}"
                )

            if isinstance(product, Product):
                setattr(product, self.IMAGE_URL_FIELD_NAME, product.image.url)
            else:
                product[self.IMAGE_URL_FIELD_NAME] = get_image_url_by_name(
                    product[self.IMAGE_FIELD_NAME]
                )

        return products
