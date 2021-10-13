from dev.commons.admin import create_default_admin
from dev.commons.db import delete_db, create_db
from dev.commons.migrations import delete_migrations_dirs


def recreate_db():
    delete_db()
    delete_migrations_dirs()
    create_db()
    create_default_admin()


custom_functions_by_args = {
    "recreate-db": recreate_db,
}
