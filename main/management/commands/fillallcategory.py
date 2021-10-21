from dataclasses import dataclass

from autoslug.utils import slugify
from django.core.management import BaseCommand
from django.db import IntegrityError

from main.models import MainCategory, Subcategory


@dataclass(frozen=True)
class Categories:
    main_category: MainCategory
    subcategories: list[Subcategory]


default_categories: list[Categories] = [
    Categories(
        MainCategory(title="Головные уборы", slug="hat"),
        [
            Subcategory(title="Кепки", slug="cap"),
            Subcategory(title="Банданы", slug="bandana"),
        ],
    ),
    Categories(
        MainCategory(title="Обувь", slug="shoes"),
        [
            Subcategory(title="Кроссовки", slug="sneakers"),
            Subcategory(title="Сандали", slug="sandals"),
        ],
    ),
    Categories(
        MainCategory(title="Верхняя одежда", slug="outerwear"),
        [
            Subcategory(title="Куртки", slug="jacket"),
            Subcategory(title="Футболки", slug="t-shirt"),
        ],
    ),
]


class Command(BaseCommand):
    help = f"Fills the database with the following categories: {default_categories}"

    def handle(self, *args, **options):
        for category in default_categories:
            try:
                category.main_category.save()
            except IntegrityError:
                pass
            for subcategory in category.subcategories:
                subcategory.main_category = category.main_category
                try:
                    subcategory.save()
                except IntegrityError:
                    pass
