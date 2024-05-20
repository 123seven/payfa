from app.models.database import create_db_and_tables, SessionLocal
from admin import Admin
from order import Order, ApiKey


def migrate() -> None:
    create_db_and_tables()

    print("Success migration!")


def create_super_admin(
    account: str = "super_admin", password: str = "super_admin_12345"
) -> None:
    Admin.create_super_admin(account, password)
    print("Success create super admin!")


if __name__ == "__main__":
    migrate()
    create_super_admin()
