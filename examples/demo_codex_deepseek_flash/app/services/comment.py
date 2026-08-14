"""Comment business logic and permissions."""

from sqlalchemy.orm import Session

from ..models.comment import Comment
from ..models.post import Post
from ..models.user import User
from ..repositories import comment as comment_repo

MAX_CONTENT_LENGTH = 2000


def create_comment(
    db: Session, *, post: Post, author: User, content: str
) -> Comment | None:
    """Create a comment on a published post; returns None when content is invalid."""
    content = content.strip()
    if not content or len(content) > MAX_CONTENT_LENGTH:
        return None
    return comment_repo.create(db, post_id=post.id, author_id=author.id, content=content)


def can_delete(user: User | None, comment: Comment) -> bool:
    """Author may delete their own comment; admins may delete any comment."""
    if user is None:
        return False
    return comment.author_id == user.id or user.is_admin

