from dataclasses import dataclass
from typing import Type

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.management import BaseCommand
from django.db.models import Model

from main.models import MainCategory, Subcategory
from main.utils.product import get_product_sub_models


@dataclass(frozen=True)
class Categories:
    main_category: MainCategory
    subcategories: list[Subcategory]


def get_content_model_type_by_model(model: Type[Model]):
    return ContentType.objects.get_for_model(model=model)


content_models = get_product_sub_models()
content_type_by_model = dict(map(
    lambda x: (x[0], get_content_model_type_by_model(x[1]))
    , content_models.items()
))

default_categories: list[Categories] = [
    Categories(
        MainCategory(title="Головные уборы", slug="hat"),
        [
            Subcategory(
                title="Кепки", slug="cap", product_model=content_type_by_model["Hat"]
            ),
            Subcategory(
                title="Банданы",
                slug="bandana",
                product_model=content_type_by_model["Hat"],
            ),
        ],
    ),
    Categories(
        MainCategory(title="Обувь", slug="shoes"),
        [
            Subcategory(
                title="Кроссовки",
                slug="sneakers",
                product_model=content_type_by_model["Shoes"],
            ),
            Subcategory(
                title="Сандали",
                slug="sandals",
                product_model=content_type_by_model["Shoes"],
            ),
        ],
    ),
    Categories(
        MainCategory(title="Верхняя одежда", slug="outerwear"),
        [
            Subcategory(
                title="Куртки",
                slug="jacket",
                product_model=content_type_by_model["Outerwear"],
            ),
            Subcategory(
                title="Футболки",
                slug="t-shirt",
                product_model=content_type_by_model["Outerwear"],
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
