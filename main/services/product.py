from typing import Type

from django.db.models import Q, QuerySet

from main.config.product import ProductServiceConfig
from main.models import Product, MainCategory, Category, Brand
from main.utils.service.product import is_valid_sex_name, get_image_url_by_name


class ProductService:
    IMAGE_FIELD_NAME = "image"
    IMAGE_URL_FIELD_NAME = "image_url"

    def __init__(self, config: Type[ProductServiceConfig] = None):
        self.__filter_options_dict = {}
        self.__filter_options_list = []
        self.__select_related_fields = []
        self.__prefetch_related_fields = []
        self.__selected_values = []
        if config is not None:
            self.set_config(config)

    def set_config(self, config: Type[ProductServiceConfig]):
        settings = config.get_config()
        select_related_fields = settings.get(config.Settings.SELECT_RELATED_FIELDS)
        prefetch_related_fields = settings.get(config.Settings.PREFETCH_RELATED_FIELDS)
        selected_values = settings.get(config.Settings.SELECTED_VALUES)

        if select_related_fields is not None:
            self._clear_select_related_field()
            self._add_select_related_fields(select_related_fields)

        if prefetch_related_fields is not None:
            self._clear_prefetched_fields()
            self._add_prefetched_fields(prefetch_related_fields)

        if selected_values is not None:
            self._clear_selected_values()
            self._add_selected_values(selected_values)

        return self

    def sex(
        self, sex_name: Product.SexChoice, include_nulls: bool = True
    ) -> "ProductService":
        if not is_valid_sex_name(sex_name):
            raise ValueError(
                f"Invalid sex name. Expected: {Product.SexChoice.values}. Now: {sex_name}"
            )
        if include_nulls:
            return self.__set_filter_options(Q(sex=sex_name) | Q(sex__isnull=True))

        return self.__set_filter_options(sex=sex_name)

    def main_category(self, main_category: MainCategory) -> "ProductService":
        return self.__set_filter_options(category__main_category=main_category)

    def category(self, category: Category) -> "ProductService":
        return self.__set_filter_options(category=category)

    def brand(self, brand: Brand) -> "ProductService":
        return self.__set_filter_options(brand=brand)

    def _add_select_related_fields(self, *args):
        self.__select_related_fields.extend(*args)
        return self

    def _clear_select_related_field(self):
        self.__select_related_fields.clear()
        return self

    def _add_prefetched_fields(self, *args):
        self.__prefetch_related_fields.extend(*args)
        return self

    def _clear_prefetched_fields(self):
        self.__prefetch_related_fields.clear()
        return self

    def _add_selected_values(self, *args) -> "ProductService":
        self.__selected_values.extend(*args)
        return self

    def _clear_selected_values(self):
        self.__selected_values.clear()
        return self

    def get_products(self) -> QuerySet[Product]:
        products = Product.objects.filter(
            *self.__filter_options_list, **self.__filter_options_dict
        )

        if self.__prefetch_related_fields:
            products = products.prefetch_related(*self.__prefetch_related_fields)

        if self.__select_related_fields:
            products = products.select_related(*self.__select_related_fields)

        if self.__selected_values:
            products = products.values(*self.__selected_values)

        products = self.__add_image_url_fields(products)
        return products

    def __set_filter_options(self, *args, **kwargs) -> "ProductService":
        self.__filter_options_list.extend(args)
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
