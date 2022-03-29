from dataclasses import dataclass

from main.models import ProductWarehouseInfo


@dataclass(frozen=True, eq=True)
class CartProductInfo:
    product_id: int
    size: ProductWarehouseInfo.SizeChoice


@dataclass(repr=True)
class CartProductInfoWithAmount:
    product_info: CartProductInfo
    amount: int = 1
