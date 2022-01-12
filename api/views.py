from ninja import NinjaAPI
from ninja.security import django_auth

from api.errors import warehouse
from api.schemas.base import SuccessJsonResponse, FailJsonResponse
from api.schemas.cart import CartProductScheme
from cart.services import CartService
from main.services import ProductWarehouseInfoService

api = NinjaAPI(csrf=True)

cart_api_prefix = "/cart/"


@api.post(cart_api_prefix + "add-products", auth=django_auth)
def add_product_view(request, cart_product: CartProductScheme):
    product_warehouse_info = (
        ProductWarehouseInfoService().get_or_none_product_warehouse_info(
            cart_product.pk, size=cart_product.size
        )
    )
    if product_warehouse_info is None:
        fail_response = FailJsonResponse(
            errors=warehouse.create_errors_report_dict(
                product_pk=cart_product.pk, size=cart_product.size
            )
        )
        return api.create_response(request, fail_response, status=404)

    CartService().add_product(request.user, product_warehouse_info)

    return SuccessJsonResponse()
