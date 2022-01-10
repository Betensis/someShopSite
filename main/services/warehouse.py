from typing import Iterable

from django.db.models import QuerySet

from main.models import ProductWarehouseInfo, Product


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
