"""Password hashing and input validation.

Uses scrypt from the standard library, so no extra dependency is needed.
Stored format: scrypt$N$r$p$salt$hash  (salt and hash are urlsafe base64).
"""

import base64
import hashlib
import hmac
import os
import re

from src.auth.exceptions import InvalidUsernameError, WeakPasswordError

SCRYPT_N = 2**14
SCRYPT_R = 8
SCRYPT_P = 1
KEY_LENGTH = 32
SALT_BYTES = 16

MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 128
USERNAME_PATTERN = re.compile(r"^[a-z0-9_.-]{3,32}$")


def _b64e(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii")


def _b64d(text: str) -> bytes:
    return base64.urlsafe_b64decode(text.encode("ascii"))


def hash_password(password: str) -> str:
    """Hash a password with a fresh random salt."""
    salt = os.urandom(SALT_BYTES)
    derived = hashlib.scrypt(
        password.encode("utf-8"),
        salt=salt,
        n=SCRYPT_N,
        r=SCRYPT_R,
        p=SCRYPT_P,
        dklen=KEY_LENGTH,
    )
    return "$".join(
        ["scrypt", str(SCRYPT_N), str(SCRYPT_R), str(SCRYPT_P), _b64e(salt), _b64e(derived)]
    )


def verify_password(password: str, stored_hash: str) -> bool:
    """Check a password against a stored hash in constant time."""
    try:
        scheme, n, r, p, salt_b64, hash_b64 = stored_hash.split("$")
        if scheme != "scrypt":
            return False
        expected = _b64d(hash_b64)
        derived = hashlib.scrypt(
            password.encode("utf-8"),
            salt=_b64d(salt_b64),
            n=int(n),
            r=int(r),
            p=int(p),
            dklen=len(expected),
        )
    except (ValueError, TypeError):
        return False
    return hmac.compare_digest(derived, expected)


def normalize_username(username: str) -> str:
    return username.strip().lower()


def validate_username(username: str) -> str:
    """Return the normalized username or raise InvalidUsernameError."""
    normalized = normalize_username(username)
    if not USERNAME_PATTERN.match(normalized):
        raise InvalidUsernameError(
            "Username must be 3-32 characters: letters, numbers, '_', '.' or '-'."
        )
    return normalized


def validate_password(password: str) -> None:
    """Raise WeakPasswordError if the password is too weak."""
    if len(password) < MIN_PASSWORD_LENGTH:
        raise WeakPasswordError(f"Password must be at least {MIN_PASSWORD_LENGTH} characters.")
    if len(password) > MAX_PASSWORD_LENGTH:
        raise WeakPasswordError(f"Password must be at most {MAX_PASSWORD_LENGTH} characters.")
    if not any(c.isalpha() for c in password) or not any(c.isdigit() for c in password):
        raise WeakPasswordError("Password must contain at least one letter and one number.")
