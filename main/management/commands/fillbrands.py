from django.core.management import BaseCommand

from main.models import Brand

default_brands = [
    "Nike",
    "Adidas",
    "Levi's",
]


class Command(BaseCommand):
    def handle(self, *args, **options):
        for brand_title in default_brands:
            Brand.objects.get_or_create(title=brand_title)
