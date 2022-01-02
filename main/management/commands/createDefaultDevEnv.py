from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    help = "Create default development environment: recreate db and fill it. Also create default admin"

    def handle(self, *args, **options):
        call_command('recreateAndFillDB')
        call_command('createDefaultAdmin')
