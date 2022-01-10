from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    help = "Recreate db and fill categories and brands"

    def handle(self, *args, **options):
        call_command("recreateDB")
        call_command("fillProducts")
        call_command("fillProductWarehouseInfos")
