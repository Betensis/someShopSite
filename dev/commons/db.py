from core.settings import DEBUG, DATABASES
from dev.commons.migrations import make_migrations, migrate


def create_db():
    make_migrations()
    migrate(run_syncdb=True)


def delete_db():
    if not DEBUG:
        raise Exception("Should set debug settings")
    db_path = DATABASES["default"]["NAME"]
    db_path.unlink(missing_ok=True)
