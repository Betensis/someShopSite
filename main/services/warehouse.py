from typing import Iterable

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from cart.entity.product_info import CartProductInfo
from main.exception import ProductNotAvailableException
from main.models import ProductWarehouseInfo, Product

User = get_user_model()


class ProductWarehouseInfoService:
    _model = ProductWarehouseInfo

    def get_product_warehouse_info_by_ids_and_size(
        self, product_infos: Iterable[CartProductInfo]
    ) -> list[ProductWarehouseInfo]:
        result = []
        for product_info in product_infos:
            result.append(
                self._model.objects.get(
                    product_id=product_info.product_id, product_size=product_info.size
                )
            )

        return result

    def decrease_product_warehouse_count(
        self, product_warehouse: ProductWarehouseInfo, amount_offset: int = 1
    ):
        if (result_count := product_warehouse.product_quantity - amount_offset) < 0:
            raise ProductNotAvailableException(
                f"Product warehouse amount after decrease must be more than 0. Now: {result_count}, "
                f"product amount: {product_warehouse.product_quantity}, amount_offset: {amount_offset}",
            )
        product_warehouse.product_quantity = result_count
        product_warehouse.save()

    @staticmethod
    def get_warehouses_by_product(product: Product) -> QuerySet[ProductWarehouseInfo]:
        return product.productwarehouseinfo_set.all()

    def is_products_available(self, products: Iterable[Product]) -> bool:
        return all(map(lambda product: self.is_product_available(product), products))

    def is_product_available(self, product: Product) -> bool:
        warehouses = self.get_warehouses_by_product(product)
        return warehouses.filter(product_quantity__gt=1).exists()

    @staticmethod
    def get_sizes_by_product(product: Product) -> list[ProductWarehouseInfo.SizeChoice]:
        return list(
            map(
                lambda products_info: products_info["product_size"],
                product.productwarehouseinfo_set.values("product_size"),
            )
        )

    @staticmethod
    def get_allowed_sizes_by_product(
        product: Product,
    ) -> list[ProductWarehouseInfo.SizeChoice]:
        return list(
            map(
                lambda products_info: products_info["product_size"],
                product.productwarehouseinfo_set.filter(product_quantity__gt=0).values(
                    "product_size"
                ),
            )
        )

    def get_allowed_sizes_by_product_id(self, product_id: int):
        return list(
            map(
                lambda products_info: products_info["product_size"],
                self._model.objects.filter(
                    product_quantity__gt=0, product_id=product_id
                ).values("product_size"),
            )
        )

    @staticmethod
    def get_or_none_product_warehouse_info(
        product_id: int, size: ProductWarehouseInfo.SizeChoice
    ):
        return ProductWarehouseInfo.objects.get_or_none(
            product__pk=product_id, product_size=size
        )
