from dataclasses import dataclass

from django.core.exceptions import ValidationError
from django.core.management import BaseCommand

from main.models import MainCategory, Subcategory
from main.utils.service.product import get_product_sub_model_content_types


@dataclass(frozen=True)
class Categories:
    main_category: MainCategory
    subcategories: list[Subcategory]


content_type_by_model = get_product_sub_model_content_types()

default_categories: list[Categories] = [
    Categories(
        MainCategory(title="Головные уборы", slug="hat"),
        [
            Subcategory(
                title="Кепки",
                slug="cap",
                product_content_type=content_type_by_model["Hat"],
            ),
            Subcategory(
                title="Банданы",
                slug="bandana",
                product_content_type=content_type_by_model["Hat"],
            ),
        ],
    ),
    Categories(
        MainCategory(title="Обувь", slug="shoes"),
        [
            Subcategory(
                title="Кроссовки",
                slug="sneakers",
                product_content_type=content_type_by_model["Shoes"],
            ),
            Subcategory(
                title="Сандали",
                slug="sandals",
                product_content_type=content_type_by_model["Shoes"],
            ),
        ],
    ),
    Categories(
        MainCategory(title="Верхняя одежда", slug="outerwear"),
        [
            Subcategory(
                title="Куртки",
                slug="jacket",
                product_content_type=content_type_by_model["Outerwear"],
            ),
            Subcategory(
                title="Футболки",
                slug="t-shirt",
                product_content_type=content_type_by_model["Outerwear"],
            ),
        ],
    ),
]


class Command(BaseCommand):
    help = f"Fills the database with the following categories: {default_categories}"

    def handle(self, *args, **options):
        for category in default_categories:
            try:
                category.main_category.validate_unique()
            except ValidationError:
                pass
            else:
                category.main_category.save()
            for subcategory in category.subcategories:
                subcategory.main_category = category.main_category
                try:
                    subcategory.validate_unique()
                except ValidationError:
                    continue
                subcategory.save()
