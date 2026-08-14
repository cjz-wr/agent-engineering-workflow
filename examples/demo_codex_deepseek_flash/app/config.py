"""Application configuration loaded from environment variables / .env file."""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def _get_bool(name: str, default: str = "false") -> bool:
    return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "on"}


class Settings:
    app_name: str = os.getenv("APP_NAME", "Mini Blog")
    app_host: str = os.getenv("APP_HOST", "0.0.0.0")
    app_port: int = int(os.getenv("APP_PORT", "8000"))
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./data/blog.db")
    secret_key: str = os.getenv("SECRET_KEY", "")
    session_ttl: int = int(os.getenv("SESSION_TTL", str(7 * 24 * 3600)))
    allow_user_publish: bool = _get_bool("ALLOW_USER_PUBLISH", "false")
    cookie_name: str = "mini_blog_session"


settings = Settings()

if not settings.secret_key:
    raise RuntimeError(
        "SECRET_KEY is not configured. Copy .env.example to .env and set a strong SECRET_KEY."
    )

