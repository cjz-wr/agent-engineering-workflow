"""Signed session cookie helpers (stdlib-only, HMAC-SHA256)."""

import base64
import hashlib
import hmac
import json
import time

from fastapi import Request, Response

from ..config import settings

_COOKIE_NAME = settings.cookie_name
_SEP = "."


def _sign(raw: bytes) -> str:
    return hmac.new(settings.secret_key.encode("utf-8"), raw, hashlib.sha256).hexdigest()


def encode_session(payload: dict) -> str:
    """Encode a payload into a signed cookie value with an expiry timestamp."""
    data = dict(payload)
    data["exp"] = int(time.time()) + settings.session_ttl
    raw = base64.urlsafe_b64encode(json.dumps(data, ensure_ascii=False).encode("utf-8")).decode("ascii")
    return raw + _SEP + _sign(raw.encode("ascii"))


def decode_session(token: str) -> dict:
    """Decode and verify a signed cookie value; returns {} when invalid or expired."""
    if not token or _SEP not in token:
        return {}
    raw, _, signature = token.partition(_SEP)
    try:
        if not hmac.compare_digest(signature, _sign(raw.encode("ascii"))):
            return {}
        payload = json.loads(base64.urlsafe_b64decode(raw.encode("ascii")).decode("utf-8"))
    except Exception:
        return {}
    if int(payload.get("exp", 0)) < int(time.time()):
        return {}
    return payload


class SessionBox:
    """In-memory view of the signed session cookie.

    Mutations are tracked and applied to the final response via ``apply_to``.
    (FastAPI does not propagate cookies set on an injected ``Response`` when the
    route returns its own ``RedirectResponse``, so the response is applied
    explicitly at the call site.)
    """

    def __init__(self, payload: dict):
        self._payload = payload
        self._dirty = False
        self._cleared = False
        self.uid: int | None = payload.get("uid")

    def login(self, uid: int) -> None:
        self._payload["uid"] = uid
        self._dirty = True

    def logout(self) -> None:
        self._cleared = True

    def add_flash(self, message: str) -> None:
        self._payload.setdefault("flash", []).append(message)
        self._dirty = True

    def pop_flashes(self) -> list[str]:
        flashes = list(self._payload.pop("flash", []))
        if flashes:
            self._dirty = True
        return flashes

    def apply_to(self, response: Response) -> None:
        """Write cookie mutations (if any) onto the final response."""
        if self._cleared:
            response.delete_cookie(_COOKIE_NAME)
        elif self._dirty:
            response.set_cookie(
                _COOKIE_NAME,
                encode_session(self._payload),
                max_age=settings.session_ttl,
                httponly=True,
                samesite="lax",
            )


def get_session(request: Request) -> SessionBox:
    """FastAPI dependency: access to the signed session cookie."""
    return SessionBox(decode_session(request.cookies.get(_COOKIE_NAME, "")))
