from api.errors.enums import ProductWarehouseInfoErrors
from api.errors.product import get_product_pk_error_report
from main.models import Product
from main.services import ProductWarehouseInfoService
from main.utils.service.product import get_max_product_pk


def get_size_error_report(
    size: str, allowed_sizes_list: list[str]
) -> tuple[dict[int, str], bool]:
    if size in allowed_sizes_list:
        return {}, False

    return {
        ProductWarehouseInfoErrors.InvalidSize.value: f"Invalid size. Allowed sizes: {allowed_sizes_list}. Now: {size}"
    }, True


def create_errors_report_dict(**kwargs) -> dict[int, str]:
    errors = {}

    product_pk = kwargs.get("product_pk")
    if product_pk is not None:
        pk_error, success_pk_validation = get_product_pk_error_report(
            product_pk, get_max_product_pk()
        )

        errors |= pk_error

    size = kwargs.get("size")
    if size is not None and success_pk_validation:
        product = Product.objects.get(pk=product_pk)
        allowed_sizes_list = ProductWarehouseInfoService().get_allowed_sizes_by_product(
            product
        )

        size_error, _ = get_size_error_report(size, allowed_sizes_list)
        errors |= size_error

    return errors
