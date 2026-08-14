"""One-click admin promotion script.

Promotes an existing user to the admin role (idempotent: already-admin users
are left unchanged). Uses the same DATABASE_URL / .env configuration as the
application.

Usage:
    .venv\\Scripts\\python promote_admin.py <username>
    .venv\\Scripts\\python promote_admin.py          # interactive prompt
"""

import sys

from app import repositories as repo
from app.db import SessionLocal
from app.models import ROLE_ADMIN


def main() -> int:
    username = (sys.argv[1] if len(sys.argv) > 1 else "").strip()
    if not username:
        username = input("Username to promote to admin: ").strip()
    if not username:
        print("[ERROR] username must not be empty")
        return 1

    db = SessionLocal()
    try:
        user = repo.user.get_by_username(db, username)
        if user is None:
            print(f"[ERROR] user '{username}' not found")
            return 1
        if user.role == ROLE_ADMIN:
            print(f"[INFO] user '{username}' is already an admin")
            return 0
        user.role = ROLE_ADMIN
        repo.user.save(db, user)
        db.commit()
        print(f"[OK] user '{username}' is now an admin")
        return 0
    finally:
        db.close()


if __name__ == "__main__":
    raise SystemExit(main())
