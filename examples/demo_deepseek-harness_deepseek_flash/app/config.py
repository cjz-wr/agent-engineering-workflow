"""Application configuration loaded from environment variables / .env file.

No secrets are hard-coded here; SECRET_KEY is required and MUST be provided
through the environment (see .env.example).
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings for the application."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Mini Blog"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    database_url: str = "sqlite:///./data/blog.db"

    # REQUIRED: session signing secret, provided via environment variable.
    secret_key: str

    # If true, users may publish their own posts; otherwise only admins publish.
    allow_user_publish: bool = False

    session_cookie_name: str = "mini_blog_session"
    session_max_age: int = 60 * 60 * 24 * 7  # 7 days

    # PBKDF2-HMAC-SHA256 iteration count for password hashing.
    password_iterations: int = 600_000


@lru_cache
def get_settings() -> Settings:
    """Return the cached application settings instance."""
    return Settings()
