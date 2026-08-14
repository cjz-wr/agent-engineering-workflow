"""Password hashing utilities.

Uses PBKDF2-HMAC-SHA256 from the standard library (no external dependency):
each password is hashed with a random per-user salt and a configurable
iteration count. The encoded format is:

    pbkdf2_sha256$<iterations>$<salt_hex>$<hash_hex>

Verification uses hmac.compare_digest to avoid timing attacks.
"""

import hashlib
import hmac
import secrets

ALGORITHM = "pbkdf2_sha256"
_DEFAULT_ITERATIONS = 600_000


def hash_password(password: str, iterations: int = _DEFAULT_ITERATIONS) -> str:
    """Hash a plaintext password and return the encoded string."""
    salt = secrets.token_hex(16)
    derived = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), bytes.fromhex(salt), iterations)
    return f"{ALGORITHM}${iterations}${salt}${derived.hex()}"


def verify_password(password: str, encoded: str) -> bool:
    """Verify a plaintext password against an encoded hash."""
    try:
        algorithm, iterations, salt, expected = encoded.split("$", 3)
    except ValueError:
        return False
    if algorithm != ALGORITHM:
        return False
    try:
        derived = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            bytes.fromhex(salt),
            int(iterations),
        )
    except (ValueError, TypeError):
        return False
    return hmac.compare_digest(derived.hex(), expected)
