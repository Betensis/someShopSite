from django.core.management import BaseCommand, call_command

fill_db_commands = [
    "fillallcategory",
    "fillbrands",
]


class Command(BaseCommand):
    help = "recreate db and fill categories and brands"

    def handle(self, *args, **options):
        call_command("recreatedb")
        for fill_command in fill_db_commands:
            call_command(fill_command)
