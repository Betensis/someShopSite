from django.db.models import QuerySet

from core import settings
from main.models import Product, MainCategory, Subcategory, Brand


class ProductService:
    IMAGE_FIELD_NAME = 'image'

    def __init__(self):
        self.__filter_options_dict = {}
        self._select_related_fields = ["brand"]
        self._prefetch_related_fields = ["info_tags"]
        self._selected_fields = []

    def sex(self, sex_name: Product.SexChoice) -> "ProductService":
        return self.__set_filter_options(sex=sex_name, sex__isnull=True)

    def main_category(self, main_category: MainCategory) -> "ProductService":
        return self.__set_filter_options(category__main_category=main_category)

    def subcategory(self, subcategory: Subcategory) -> "ProductService":
        return self.__set_filter_options(category=subcategory)

    def brand(self, brand: Brand) -> "ProductService":
        return self.__set_filter_options(brand=brand)

    def selected_fields(self, *args):
        self._selected_fields.extend(args)
        return self

    def get_products(self) -> QuerySet[Product]:
        products = Product.objects.filter(**self.__filter_options_dict)

        if self._prefetch_related_fields:
            products = products.prefetch_related(*self._prefetch_related_fields)
        if self._select_related_fields:
            products = products.select_related(*self._select_related_fields)

        if self._selected_fields:
            products = products.values(*self._selected_fields)
            if self.IMAGE_FIELD_NAME in self._selected_fields:
                products = self.__add_image_url_fields(products)

        return products

    def __set_filter_options(self, **kwargs) -> "ProductService":
        self.__filter_options_dict.update(kwargs)
        return self

    def __add_image_url_fields(self, products: QuerySet[Product]):
        for product in products:
            product['image_url'] = settings.MEDIA_URL + product[self.IMAGE_FIELD_NAME]

        return products