from ninja import Schema

from main.models import ProductWarehouseInfo


class CartProductScheme(Schema):
    pk: int
    size: ProductWarehouseInfo.SizeChoice
