from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Recreates migrations and creates a database."

    def handle(self, *args, **options):
        call_command("flush", database="default")
        call_command("deletemigrationsdir")
        call_command("makemigrations", 'main')
        call_command("migrate", "--run-syncdb")
