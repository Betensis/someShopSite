from dataclasses import dataclass

from django.core.exceptions import ValidationError
from django.core.management import BaseCommand

from main.models import MainCategory, Subcategory


@dataclass
class Categories:
    main_category: MainCategory
    subcategories: list[Subcategory]


default_categories: list[Categories] = [
    Categories(
        MainCategory(title="Головные уборы", slug="hat"),
        [
            Subcategory(
                title="Кепки",
                slug="cap",
            ),
            Subcategory(
                title="Банданы",
                slug="bandana",
            ),
            Subcategory(
                title="Шапки",
                slug="hat",
            ),
            Subcategory(
                title="Балаклава",
                slug="balaklava",
            ),
        ],
    ),
    Categories(
        MainCategory(title="Обувь", slug="shoes"),
        [
            Subcategory(
                title="Кроссовки",
                slug="sneakers",
            ),
            Subcategory(
                title="Сандали",
                slug="sandals",
            ),
        ],
    ),
    Categories(
        MainCategory(title="Верхняя одежда", slug="outerwear"),
        [
            Subcategory(
                title="Куртки",
                slug="jacket",
            ),
            Subcategory(
                title="Футболки",
                slug="t-shirt",
            ),
            Subcategory(
                title="Худи",
                slug="hoodies",
            ),
        ],
    ),
]


class Command(BaseCommand):
    help = f"Fills the database with the following categories: {default_categories}"

    def handle(self, *args, **options):
        for category in default_categories:
            category.main_category, _ = MainCategory.objects.get_or_create(
                title=category.main_category, slug=category.main_category.slug
            )

            for subcategory in category.subcategories:
                subcategory.main_category = category.main_category
                try:
                    subcategory.validate_unique()
                except ValidationError:
                    continue
                subcategory.save()

        self.stdout.write(self.style.SUCCESS("Successfully filled categories"))
