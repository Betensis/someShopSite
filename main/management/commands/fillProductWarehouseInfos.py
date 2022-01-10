from dataclasses import dataclass

from django.core.management import BaseCommand

from main.models import ProductWarehouseInfo, Product


SexChoice = ProductWarehouseInfo.SizeChoice


@dataclass
class WarehouseInfo:
    product: Product
    size_quantity_list: list[tuple[ProductWarehouseInfo.SizeChoice, int]]


warehouses_info: list[WarehouseInfo] = [
    WarehouseInfo(
        Product(title="Черная шапка из искусственного меха Kavu Fud"),
        [
            (SexChoice.M, 1),
            (SexChoice.L, 3),
        ],
    ),
    WarehouseInfo(
        Product(
            title="Белые высокие кроссовки с красными вставками Pull&Bear Space Jam"
        ),
        [(SexChoice.S, 5), (SexChoice.XS, 0)],
    ),
    WarehouseInfo(
        Product(
            title="Джоггеры для дома в темно-синюю и зеленую полоску с контрастным поясом с логотипом GANT"
        ),
        [
            (SexChoice.XL, 1),
            (SexChoice.M, 4),
        ],
    ),
    WarehouseInfo(
        Product(title="Черная укороченная куртка ellesse"),
        [(SexChoice.M, 0), (SexChoice.XS, 5), (SexChoice.L, 3)],
    ),
]


class Command(BaseCommand):
    help = f"Fills the database with the following warehouses info: {warehouses_info}"

    def handle(self, *args, **options):
        for warehouse_info in warehouses_info:
            try:
                product = Product.objects.get(title=warehouse_info.product.title)
            except Product.DoesNotExist:
                self.stderr.write(f"Product: {warehouse_info.product} already exist")

            for size, quantity in warehouse_info.size_quantity_list:
                ProductWarehouseInfo.objects.get_or_create(
                    product=product, product_size=size, product_quantity=quantity
                )

        self.stdout.write(self.style.SUCCESS("Successfully filled warehouses info"))
