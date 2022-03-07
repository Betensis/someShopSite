from typing import Iterable

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from main.models import ProductWarehouseInfo, Product

User = get_user_model()


class ProductWarehouseInfoService:
    _model = ProductWarehouseInfo

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
