"""Custom exceptions for the auth module."""


class AuthError(Exception):
    """Base class for all authentication errors."""


class InvalidUsernameError(AuthError):
    """The username does not meet the format rules."""


class WeakPasswordError(AuthError):
    """The password does not meet the strength rules."""


class UsernameTakenError(AuthError):
    """A user with this username already exists."""


class InvalidCredentialsError(AuthError):
    """Wrong username or password (deliberately does not say which)."""

    def __init__(self, message: str = "Invalid username or password."):
        super().__init__(message)


class AccountLockedError(AuthError):
    """Too many failed attempts; the account is temporarily locked."""

    def __init__(self, retry_after: int):
        self.retry_after = retry_after
        super().__init__(f"Account temporarily locked. Try again in {retry_after} seconds.")
