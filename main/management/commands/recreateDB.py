from pathlib import Path

from django.core.management import call_command
from django.core.management.base import BaseCommand

from core import settings
from core.settings import APPS


def delete_db():
    if settings.DEBUG:
        db_name = settings.DATABASES["default"]["NAME"]
        if type(db_name) != Path:
            return

        db_name.unlink()


class Command(BaseCommand):
    help = "Recreates migrations and creates a database."

    def handle(self, *args, **options):
        delete_db()
        call_command("deleteMigrationDirs")
        call_command("makemigrations", *APPS)
        call_command("migrate", "--run-syncdb")

        self.stdout.write(self.style.SUCCESS("Database recreated"))
