from django.core.management import BaseCommand

from main.models import MainCategory

default_main_categories = [
    "Головные уборы",
    "Обувь",
    "Верхняя одежда",
    "Аксессуары",
]


class Command(BaseCommand):
    def handle(self, *args, **options):
        for main_category_title in default_main_categories:
            MainCategory.objects.get_or_create(title=main_category_title)
