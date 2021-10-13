from shutil import rmtree

from django.core.management import call_command

from dev.settings import apps, apps_path


def make_migrations():
    call_command("makemigrations", *apps)


def delete_migrations_dirs():
    for app_path in apps_path:
        migration_dir = app_path.joinpath("migrations")
        if migration_dir.exists():
            rmtree(migration_dir.resolve())


def migrate(run_syncdb=True):
    if run_syncdb:
        call_command("migrate", "--run-syncdb")
    call_command("migrate")
