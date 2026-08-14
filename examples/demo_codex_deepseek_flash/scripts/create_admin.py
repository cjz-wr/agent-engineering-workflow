"""Create or promote an admin user.

Usage:
    python scripts/create_admin.py <username> [password]

When the password is omitted, it is read interactively.
"""

import getpass
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.db import SessionLocal, init_db  # noqa: E402
from app.repositories import user as user_repo  # noqa: E402
from app.services import auth as auth_service  # noqa: E402


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python scripts/create_admin.py <username> [password]")
        return 2

    username = sys.argv[1].strip()
    if not username:
        print("Username must not be empty.")
        return 2
    password = sys.argv[2] if len(sys.argv) > 2 else None
    if password is None:
        password = getpass.getpass("Password: ")
    if not password:
        print("Password must not be empty.")
        return 2

    init_db()
    db = SessionLocal()
    try:
        user = user_repo.get_by_username(db, username)
        if user is not None:
            user.role = "admin"
            db.commit()
            print(f"Promoted '{username}' to admin.")
        else:
            user_repo.create(
                db,
                username=username,
                password_hash=auth_service.hash_password(password),
                display_name=username,
                role="admin",
            )
            db.commit()
            print(f"Created admin user '{username}'.")
    finally:
        db.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

