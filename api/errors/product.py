from api.errors.enums import ProductErrors


def get_product_pk_error_report(pk: int, max_pk: int) -> tuple[dict[int, str], bool]:
    if pk <= 0:
        return {
            ProductErrors.InvalidPk.value: f"Invalid pk. Pk must be > 0. Now: {pk = }"
        }, False
    if pk > max_pk:
        return {
            ProductErrors.InvalidPk.value: f"Invalid pk. Max pk is {max_pk}. Pk given: {pk = }"
        }, False

    return {}, True