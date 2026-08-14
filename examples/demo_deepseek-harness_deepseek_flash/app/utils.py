"""Small shared helpers."""

from datetime import datetime, timezone

# SQLite stores naive datetimes; keep UTC values naive for consistency with
# server_default=func.now() (SQLite CURRENT_TIMESTAMP).
def utcnow() -> datetime:
    """Return the current UTC time as a naive datetime."""
    return datetime.now(timezone.utc).replace(tzinfo=None)
