"""Post model and article lifecycle status constants.

Lifecycle: draft -> submitted -> published / rejected.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

STATUS_DRAFT = "draft"
STATUS_SUBMITTED = "submitted"
STATUS_PUBLISHED = "published"
STATUS_REJECTED = "rejected"

# Statuses reachable through public routes.
PUBLIC_STATUSES = (STATUS_PUBLISHED,)


class Post(Base):
    """An article written by a user."""

    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(200), unique=True, index=True, nullable=False)
    content: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(20), default=STATUS_DRAFT, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )
    published_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    author: Mapped["User"] = relationship(back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship(back_populates="post", cascade="all, delete-orphan")

    @property
    def is_published(self) -> bool:
        return self.status == STATUS_PUBLISHED
