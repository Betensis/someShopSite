from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.db import IntegrityError


class Command(BaseCommand):
    help = "Create default admin. Login: admin, password: 111111, email admin@gmail.com"

    def handle(self, *args, **options):
        User = get_user_model()
        try:
            User.objects.create_superuser(
                username="admin", email="admin@mail.com", password="111111"
            )
        except IntegrityError:
            print("User already exist")
