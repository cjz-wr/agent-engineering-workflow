"""SQLAlchemy engine, session factory and declarative base.

SQLite is the default backend (see DATABASE_URL). The Base class is shared by
all models in app.models.
"""

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import get_settings


class Base(DeclarativeBase):
    """Declarative base for all ORM models."""


settings = get_settings()

_connect_args: dict = {}
if settings.database_url.startswith("sqlite"):
    # FastAPI runs route handlers in a thread pool; allow cross-thread reuse.
    _connect_args = {"check_same_thread": False}

engine = create_engine(settings.database_url, connect_args=_connect_args)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


def get_db():
    """FastAPI dependency yielding a database session."""
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Create the database file directory (SQLite) and all tables."""
    if settings.database_url.startswith("sqlite"):
        # sqlite:///./data/blog.db -> ./data
        db_path = settings.database_url.replace("sqlite:///", "", 1)
        if db_path and db_path != ":memory:":
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    # Import models so their tables are registered on Base.metadata.
    from app import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
