from dataclasses import dataclass

from django.core.exceptions import ValidationError
from django.core.management import BaseCommand

from main.models import MainCategory, Category


@dataclass
class Categories:
    main_category: MainCategory
    subcategories: list[Category]


default_categories: list[Categories] = [
    Categories(
        MainCategory(title="Головные уборы", slug="hat"),
        [
            Category(
                title="Кепки",
                slug="cap",
            ),
            Category(
                title="Банданы",
                slug="bandana",
            ),
            Category(
                title="Шапки",
                slug="hat",
            ),
            Category(
                title="Балаклава",
                slug="balaklava",
            ),
        ],
    ),
    Categories(
        MainCategory(title="Обувь", slug="shoes"),
        [
            Category(
                title="Кроссовки",
                slug="sneakers",
            ),
            Category(
                title="Сандали",
                slug="sandals",
            ),
        ],
    ),
    Categories(
        MainCategory(title="Верхняя одежда", slug="outerwear"),
        [
            Category(
                title="Куртки",
                slug="jacket",
            ),
            Category(
                title="Футболки",
                slug="t-shirt",
            ),
            Category(
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
