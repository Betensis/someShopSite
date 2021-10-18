from autoslug.utils import slugify
from django.core.management import BaseCommand

from main.models import MainCategory, Subcategory

default_categories = {
    "Головные уборы": [
        "Кепки",
        "Банданы",
    ],
    "Обувь": [
        "Кроссовки",
        "Сандали",
    ],
    "Верхняя одежда": [
        "Куртки",
        "Футболки",
    ],
    "Аксессуары": ["Брелки", "Чехлы"],
}


class Command(BaseCommand):
    help = f'Fills the database with the following categories: {default_categories}'

    def handle(self, *args, **options):
        for main_category, subcategories in default_categories.items():
            main_category, _ = MainCategory.objects.get_or_create(title=main_category)
            for subcategory in subcategories:
                Subcategory.objects.get_or_create(
                    title=subcategory,
                    main_category=main_category,
                    slug=slugify(subcategory),
                )
