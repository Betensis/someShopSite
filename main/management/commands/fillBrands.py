from django.core.management import BaseCommand

from main.models import Brand

default_brands = [
    "Nike",
    "Adidas",
    "Levi's",
    "Запорожец Heritage",
    "Mark Formelle",
    "Pull&Bear",
]


class Command(BaseCommand):
    help = f"Fills the database with the following brands: {default_brands}"

    def handle(self, *args, **options):
        for brand_title in default_brands:
            Brand.objects.get_or_create(title=brand_title)
        self.stdout.write(self.style.SUCCESS("Successfully filled brands"))
