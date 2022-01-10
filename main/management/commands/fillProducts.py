from dataclasses import dataclass

from django.core.exceptions import ValidationError
from django.core.management import BaseCommand, call_command

from main.models import Brand, Category, Product, ProductInfoTags


@dataclass
class ProductWithInfo:
    product: Product
    info_tags_titles: list[str]


other_fill_commands = [
    "fillBrands",
    "fillCategories",
    "fillInfoTags",
]

nike_brand = Brand(title="Nike")
pull_n_bear_brand = Brand(title="Pull&Bear")
adidas_brand = Brand(title="Adidas")
kavu_brand = Brand(title="Kavu")
gant_brand = Brand(title="GANT")
ellesse_brand = Brand(title="ellesse")

cap_category = Category(slug="cap")
hat_category = Category(slug="hat")
balaklava_category = Category(slug="balaklava")
ushanka_category = Category(slug="ushanka")
sneakers_category = Category(slug="sneakers")
hoodies_category = Category(slug="hoodies")
joggers_category = Category(slug="joggers")

products_with_info: list[ProductWithInfo] = [
    ProductWithInfo(
        Product(
            title="Черная шапка из искусственного меха Kavu Fud",
            price=3390.00,
            description="Плотная ткань\n"
            "Подкладка из искусственного меха\n"
            "Основная часть: 50% хлопок, 50% полиэстер.\n",
            care="Протирать влажной тканевой салфеткой или губкой",
            sex="man",
            brand=nike_brand,
            category=ushanka_category,
            image="24232596-1-fadedblack.webp",
        ),
        [
            "Последний штрих",
            "Куполообразный верх",
            "С отворотом",
            "С ушами",
        ],
    ),
    ProductWithInfo(
        Product(
            title="Белые высокие кроссовки с красными вставками Pull&Bear Space Jam",
            brand=pull_n_bear_brand,
            care="Не стирать в стиральной машине",
            description="Верх из искусственной кожи\n\n"
            "Подкладка: 100% полиэстер. Подошва: 100% резина. Верх: 76% полиуретан, 24% резина.",
            price=2490.00,
            category=sneakers_category,
            image="201114408-1-multi.jpeg",
        ),
        [
            "Так и просятся в корзину покупок",
            "Дизайн Space Jam",
            "Высокий дизайн",
            "Вспомогательные петли для легкого надевания",
            "На шнуровке",
            "Язычок и задник с мягкими вставками",
            "Прочная резиновая подошва снаружи",
            "Рифленая подошва",
        ],
    ),
    ProductWithInfo(
        Product(
            title="Джоггеры для дома в темно-синюю и зеленую полоску с контрастным поясом с логотипом GANT",
            brand=gant_brand,
            price=4090.00,
            care="Машинная стирка согласно инструкции на этикетке",
            sex="man",
            category=joggers_category,
            image="200784071-1-navy.webp",
            description="Невесомый хлопок\n"
            "GANT гордится участием в проекте The Better Cotton Initiative\n"
            "Улучшенный хлопок поставляется через систему Mass Balance.",
        ),
        [
            "Из подборки экологичной моды",
            "В полоску",
            "Эластичный пояс с логотипом бренда",
            "Боковые карманы",
            "Прямой крой",
        ],
    ),
    ProductWithInfo(
        Product(
            title="Черная укороченная куртка ellesse",
            brand=ellesse_brand,
            price=2590.00,
            sex="woman",
            care="Машинная стирка согласно инструкции на этикетке",
            category=hoodies_category,
            image="23521746-2.webp",
            description="Мягкая саржа\n"
            "Легкий фактурный материал в параллельный рубчик\n"
            "Основная часть: 100% хлопок.",
        ),
        [
            "Эксклюзивно для ASOS 4505",
            "Широкий воротник",
            "Застежка на кнопки",
            "Вышивка логотипа на груди",
            "Укороченная длина",
            "Классическая крой",
        ],
    ),
]


class Command(BaseCommand):
    help = f"Fills the database with the following products: {products_with_info}"

    def handle(self, *args, **options):
        for command in other_fill_commands:
            call_command(command)

        def prepare_product(product):
            product.category = Category.objects.get(slug=product.category.slug)
            product.brand = Brand.objects.get(title=product.brand.title)

        for product_with_info in products_with_info:
            prepare_product(product_with_info.product)
            try:
                product_with_info.product.validate_unique()
            except ValidationError:
                continue

            product_with_info.product.save()
            product_with_info.product.info_tags.set(
                map(
                    lambda info_title: ProductInfoTags.objects.get(title=info_title),
                    product_with_info.info_tags_titles,
                )
            )

        self.stdout.write(self.style.SUCCESS("Successfully filled products"))
