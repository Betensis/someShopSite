from django.core.exceptions import ValidationError
from django.core.management import BaseCommand, call_command

from main.models import Brand, Subcategory, Product

other_fill_commands = [
    "fillBrands",
    "fillCategories",
]

nike_brand = Brand(title="Nike")
zaporojets_brand = Brand(title="Запорожец Heritage")
mark_formelle_brand = Brand(title="Mark Formelle")
pull_n_bear_brand = Brand(title="Pull&Bear")
adidas_brand = Brand(title="Adidas")


cap_category = Subcategory(slug="cap")
hat_category = Subcategory(slug="hat")
balaklava_category = Subcategory(slug="balaklava")

sneakers_category = Subcategory(slug="sneakers")

hoodies_category = Subcategory(slug="hoodies")


products = [
    Product(
        title="U NSW H86 SWOOSH WASH CAP",
        price=1899,
        brand=nike_brand,
        category=cap_category,
        image="U NSW H86 SWOOSH WASH CAP.webp",
    ),
    Product(
        title="Шапка Ushanka Beanie",
        price=1890,
        brand=zaporojets_brand,
        category=hat_category,
        image="MP002XU04TC8_16128390_1_v1.jpg",
    ),
    Product(
        title="Балаклава Mark",
        price=599,
        brand=mark_formelle_brand,
        category=balaklava_category,
        image="MP002XU04QHK_15883563_1_v1.webp",
    ),
    Product(
        title="Кросовки Pull&Bear",
        brand=pull_n_bear_brand,
        price=1999,
        category=sneakers_category,
        image="IX001XM00DKS_14953164_1_v1.jpeg",
    ),
    Product(
        title="Кроссовки FIREWALKER",
        brand=adidas_brand,
        price=8999,
        category=sneakers_category,
        image="RTLAAY648701_15955535_1_v1.jpg",
    ),
    Product(
        title="Худи Pull&Bear",
        brand=pull_n_bear_brand,
        price=2299,
        category=hoodies_category,
        image="IX001XM00EG4_15401957_1_v1.jpeg",
    ),
    Product(
        title="Футболка PnB",
        brand=pull_n_bear_brand,
        price=599,
        category=hoodies_category,
        image="IX001XM00DIF_14919549_1_v2.webp",
    ),
]


class Command(BaseCommand):
    help = f"Fills the database with the following products: {products}"

    def handle(self, *args, **options):
        for command in other_fill_commands:
            call_command(command)

        def prepare_product(product):
            product.category = Subcategory.objects.get(slug=product.category.slug)
            product.brand = Brand.objects.get(title=product.brand.title)

        for product in products:
            prepare_product(product)
            try:
                product.validate_unique()
            except ValidationError:
                continue

            product.save()

        self.stdout.write(self.style.SUCCESS("Successfully filled products"))
