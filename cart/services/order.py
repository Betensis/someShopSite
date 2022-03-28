from django.db import transaction

from cart.entity.cart import Cart
from cart.models import Order
from cart.services import CartService
from main.exception import ProductNotAvailableException
from main.services import ProductWarehouseInfoService


class OrderService:
    _model = Order

    def __init__(self):
        self.cart_service = CartService()
        self.product_warehouse_service = ProductWarehouseInfoService()

    @transaction.atomic
    def create_order_by_cart(
        self, request, cart: Cart, email: str, phone: str, place: str
    ):
        product_warehouse_infos = self.cart_service.get_all_product_infos_by_cart(cart)

        order = self._model(user=cart.user)
        order.contact_phone = phone
        order.contact_email = email
        order.contact_place = place
        order.save()
        order.products_warehouse_info.add(*product_warehouse_infos)

        for product_warehouse_info in order.products_warehouse_info.all():
            try:
                self.product_warehouse_service.decrease_product_warehouse_count(
                    product_warehouse_info, amount_offset=1
                )
            except ProductNotAvailableException:
                self.cart_service.delete_product_by_params_from_cart(
                    request,
                    cart,
                    product_warehouse_info.product_id,
                    product_warehouse_info.product_size,
                )
                raise

        return order

    def delete_order(self, order: Order):
        order.delete()
