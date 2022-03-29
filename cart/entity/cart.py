import dataclasses

from django.contrib.auth import get_user_model

from .product_info import CartProductInfoWithAmount, CartProductInfo
from ..exceptions import CartError

User = get_user_model()


@dataclasses.dataclass
class Cart:
    user: User
    products: list[CartProductInfoWithAmount] = dataclasses.field(default_factory=list)

    def add_product(self, product_info: CartProductInfo):
        for product_info_with_amount in self.products:
            if product_info == product_info_with_amount.product_info:
                product_info_with_amount.amount += 1
                return

        self.products.append(CartProductInfoWithAmount(product_info=product_info))

    def delete_product(self, product_info: CartProductInfo):
        product_info_list = list(
            filter(lambda x: x.product_info == product_info, self.products)
        )
        if not product_info_list:
            raise CartError("Product does not exist in this cart")

        self.products.remove(product_info_list[0])
