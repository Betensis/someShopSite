from django.http import JsonResponse
from ninja import NinjaAPI

from api.errors import warehouse
from api.errors.warehouse import create_errors_report_dict
from api.schemas.base import SuccessJsonResponse, BaseJsonResponse, FailJsonResponse
from api.schemas.cart import CartProductScheme
from main.models import ProductWarehouseInfo
from main.services import ProductWarehouseInfoService, ProductService

api = NinjaAPI()


@api.post("/add-products")
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

    return SuccessJsonResponse()
