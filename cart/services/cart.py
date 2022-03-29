from typing import Iterable

from django.contrib.auth import get_user_model
from django.http import HttpRequest
from djmoney.money import Money

from cart.entity.cart import Cart
from cart.entity.product_info import CartProductInfo
from cart.exceptions import CartDoesNotExist
from main.models import ProductWarehouseInfo
from main.services import ProductService, ProductWarehouseInfoService
from main.utils.list import get_value_by_rule

User = get_user_model()


class CartService:
    __CART_SESSION_KEY = "cart"

    def __init__(self):
        self.product_service = ProductService()
        self.product_warehouse_service = ProductWarehouseInfoService()

    def delete_product_by_params_from_cart(
        self,
        request,
        cart: Cart,
        product_id: int,
        product_size: ProductWarehouseInfo.SizeChoice,
    ):
        cart.delete_product(CartProductInfo(product_id=product_id, size=product_size))
        self.save_cart(request, cart)

    def get_cart(self, request: HttpRequest):
        cart = request.session.get(self.__CART_SESSION_KEY, None)
        if cart is None:
            raise CartDoesNotExist("Cart in session does not exist")

        return cart

    def get_or_create_cart(self, request: HttpRequest) -> tuple[Cart, bool]:
        try:
            cart = self.get_cart(request)
        except CartDoesNotExist:
            return self.create_cart(request), True

        return cart, False

    def create_cart(self, request: HttpRequest) -> Cart:
        cart = Cart(user=request.user, products=[])
        self.save_cart(request, cart)
        return cart

    def __get_product_infos_by_cart(self, cart: Cart) -> Iterable[CartProductInfo]:
        return map(
            lambda product_info_with_amount: product_info_with_amount.product_info,
            cart.products,
        )

    def is_product_in_cart(self, cart: Cart, product_info: CartProductInfo) -> bool:
        return product_info in self.__get_product_infos_by_cart(cart)

    def add_product_to_cart(
        self, request: HttpRequest, product_info: CartProductInfo
    ) -> None:
        cart, _ = self.get_or_create_cart(request)
        cart.add_product(product_info)
        self.save_cart(request, cart)

    def add_product(
        self,
        request: HttpRequest,
        product_info: CartProductInfo,
    ):
        if not request.user.is_authenticated:
            raise ValueError("User must be authenticated")

        return self.add_product_to_cart(request, product_info)

    def get_products_price_sum(self, cart: Cart) -> Money:
        product_ids = list(
            map(
                lambda product_info_with_amount: product_info_with_amount.product_info.product_id,
                cart.products,
            )
        )
        products = self.product_service.ids_in(product_ids).get_products()

        price_sum = 0
        cart_products = cart.products
        for product in products:
            price_sum += (
                product.price
                * get_value_by_rule(
                    cart_products, lambda x: x.product_info.product_id == product.id
                ).amount
            )
        return price_sum

    def get_all_product_infos_by_cart(self, cart: Cart) -> list[ProductWarehouseInfo]:
        return self.product_warehouse_service.get_product_warehouse_info_by_ids_and_size(
            map(
                lambda product_info_with_amount: product_info_with_amount.product_info,
                cart.products,
            )
        )

    def save_cart(self, request: HttpRequest, cart: Cart):
        request.session[self.__CART_SESSION_KEY] = cart
