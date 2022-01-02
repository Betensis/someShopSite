from django.core.management import call_command
from django.core.management.base import BaseCommand

from core import settings


def delete_db():
    if settings.DEBUG:
        settings.DATABASES["default"]["NAME"].unlink(missing_ok=True)


class Command(BaseCommand):
    help = "Recreates migrations and creates a database."

    def handle(self, *args, **options):
        delete_db()
        call_command("deleteMigrationDirs")
        call_command("makemigrations", "main")
        call_command("migrate", "--run-syncdb")

        self.stdout.write(self.style.SUCCESS("Database recreated"))
