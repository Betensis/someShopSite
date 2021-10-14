from shutil import rmtree

from django.core.management import BaseCommand

from core.settings import APPS, BASE_DIR


class Command(BaseCommand):
    help = 'Delete migrations from apps'

    def handle(self, *args, **options):
        for app in APPS:
            migrations_dir = BASE_DIR.joinpath(app).joinpath('migrations')
            if migrations_dir.exists() and migrations_dir.is_dir():
                rmtree(migrations_dir)
