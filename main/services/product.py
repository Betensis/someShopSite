from itertools import zip_longest

from main.models import Product
from main.utils.commons import remove_none
from main.utils.product import get_product_sub_models


class ProductService:
    @classmethod
    def get_all_products(cls, *, for_kids: bool) -> list[Product]:
        products_models = get_product_sub_models().values()
        products = map(
            lambda x: list(x.objects.filter(is_for_kids=for_kids)), products_models
        )
        result = []
        for items in zip_longest(*products):
            result.extend(items)
        return remove_none(result)
