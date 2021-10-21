from autoslug.utils import slugify
from django.core.management import BaseCommand
from django.db import IntegrityError

from main.models import MainCategory, Subcategory

default_categories: dict[MainCategory: list[Subcategory]] = {
    MainCategory(title="Головные уборы", slug="hat", pk=1): [
        Subcategory(title="Кепки", slug="cap"),
        Subcategory(title="Банданы", slug="bandana"),
    ],
    MainCategory(title="Обувь", slug="shoes", pk=2): [
        Subcategory(title="Кроссовки", slug="sneakers"),
        Subcategory(title="Сандали", slug="sandals"),
    ],
    MainCategory(title="Верхняя одежда", slug="outerwear", pk=3): [
        Subcategory(title="Куртки", slug="jacket"),
        Subcategory(title="Футболки", slug="t-shirt"),
    ],
}


class Command(BaseCommand):
    help = f"Fills the database with the following categories: {default_categories}"

    def handle(self, *args, **options):
        for main_category, subcategories in default_categories.items():
            try:
                main_category.save()
            except IntegrityError:
                pass
            for subcategory in subcategories:
                subcategory.main_category = main_category
                try:
                    subcategory.save()
                except IntegrityError:
                    pass
