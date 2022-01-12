from typing import Optional

from django.contrib.auth import get_user_model
from django.db.models import QuerySet, Sum

from cart.models import Cart
from main.models import ProductWarehouseInfo
from main.services import ProductWarehouseInfoService

User = get_user_model()


class CartService:
    def get_products_count_from_current_cart(self, user: User):
        cart = Cart.objects.get_or_none(user=user)
        if cart is None:
            return 0
        return cart.products_warehouse_info.all().count()

    def get_cart(self, user: User) -> Optional[Cart]:
        """
        :return: current cart (cart with is_bought attr equals False) or None
        """
        return Cart.objects.get_or_none(user=user)

    def get_or_create_cart(self, user: User) -> tuple[Cart, bool]:
        return Cart.objects.get_or_create(user=user)

    @staticmethod
    def add_product_to_cart(cart: Cart, product_info: ProductWarehouseInfo):
        product_warehouse_info_service = ProductWarehouseInfoService()
        if not product_warehouse_info_service.is_product_available(
            product_info.product
        ):
            raise ValueError(
                f"Product {product_info.product} with id={product_info.product.pk} unavailable. Can't add it to cart"
            )
        cart.products_warehouse_info.add(product_info)

    def add_product(
        self,
        user: User,
        product_info: ProductWarehouseInfo,
        create_cart_if_not_exist: bool = True,
    ):
        if not user.is_authenticated:
            raise ValueError("User must be authenticated")

        cart = self.get_cart(user)
        if cart is None:
            if not create_cart_if_not_exist:
                raise ValueError(f"Cart doesnt exist and {create_cart_if_not_exist = }")
            cart = Cart.objects.create(user=user)

        return self.add_product_to_cart(cart, product_info)

    @staticmethod
    def get_products_sum(cart: Cart):
        product_infos = cart.products_warehouse_info.prefetch_related("product").all()
        return product_infos.aggregate(Sum("product__price"))["product__price__sum"]

    @staticmethod
    def get_all_product_infos_by_cart(cart: Cart) -> QuerySet[ProductWarehouseInfo]:
        return cart.products_warehouse_info.all()
