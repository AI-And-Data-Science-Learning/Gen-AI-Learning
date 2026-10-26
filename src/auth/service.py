"""Registration and login logic."""

import sqlite3
import time
from functools import lru_cache
from typing import Callable

from src.auth.exceptions import (
    AccountLockedError,
    InvalidCredentialsError,
    UsernameTakenError,
)
from src.auth.models import User
from src.auth.security import (
    hash_password,
    normalize_username,
    validate_password,
    validate_username,
    verify_password,
)
from src.auth.storage import UserStore

MAX_FAILED_ATTEMPTS = 5
LOCKOUT_SECONDS = 15 * 60


@lru_cache(maxsize=1)
def _dummy_hash() -> str:
    """A throwaway hash, used so unknown usernames take as long as real ones."""
    return hash_password("dummy-password-for-timing")


class AuthService:
    def __init__(self, store: UserStore | None = None, clock: Callable[[], float] = time.time):
        self.store = store or UserStore()
        self._clock = clock

    def register(self, username: str, password: str) -> str:
        """Create a new user and return the normalized username."""
        username = validate_username(username)
        validate_password(password)
        try:
            self.store.add_user(username, hash_password(password))
        except sqlite3.IntegrityError:
            raise UsernameTakenError("That username is already taken.") from None
        return username

    def login(self, username: str, password: str) -> User:
        """Return the User on success, or raise an AuthError."""
        user = self.store.get_user(normalize_username(username))

        if user is None:
            verify_password(password, _dummy_hash())
            raise InvalidCredentialsError()

        now = self._clock()
        if user.locked_until > now:
            raise AccountLockedError(retry_after=int(user.locked_until - now) + 1)

        if not verify_password(password, user.password_hash):
            attempts = user.failed_attempts + 1
            if attempts >= MAX_FAILED_ATTEMPTS:
                self.store.set_login_state(user.id, 0, now + LOCKOUT_SECONDS)
            else:
                self.store.set_login_state(user.id, attempts, 0.0)
            raise InvalidCredentialsError()

        if user.failed_attempts or user.locked_until:
            self.store.set_login_state(user.id, 0, 0.0)
        return user
