"""Unit tests for the auth module."""

import sqlite3

import pytest

from src.auth import (
    AccountLockedError,
    AuthService,
    InvalidCredentialsError,
    InvalidUsernameError,
    UsernameTakenError,
    UserStore,
    WeakPasswordError,
)
from src.auth.security import hash_password, verify_password
from src.auth.service import LOCKOUT_SECONDS, MAX_FAILED_ATTEMPTS

GOOD_PASSWORD = "correct-horse-9"


class FakeClock:
    def __init__(self, now: float = 1_000_000.0):
        self.now = now

    def __call__(self) -> float:
        return self.now


@pytest.fixture
def clock():
    return FakeClock()


@pytest.fixture
def db_path(tmp_path):
    return str(tmp_path / "auth.db")


@pytest.fixture
def service(db_path, clock):
    return AuthService(UserStore(db_path), clock=clock)


# ---------- password hashing ----------

def test_hash_is_salted_and_verifiable():
    first, second = hash_password(GOOD_PASSWORD), hash_password(GOOD_PASSWORD)
    assert first != second
    assert verify_password(GOOD_PASSWORD, first)
    assert not verify_password("wrong-password-1", first)


@pytest.mark.parametrize("garbage", ["", "plaintext", "scrypt$1$2", "md5$a$b$c$d$e"])
def test_verify_rejects_malformed_hashes(garbage):
    assert verify_password(GOOD_PASSWORD, garbage) is False


# ---------- registration ----------

def test_register_returns_normalized_username(service):
    assert service.register("  Alice  ", GOOD_PASSWORD) == "alice"


def test_register_duplicate_is_case_insensitive(service):
    service.register("alice", GOOD_PASSWORD)
    with pytest.raises(UsernameTakenError):
        service.register("ALICE", GOOD_PASSWORD)


@pytest.mark.parametrize("bad", ["", "ab", "has space", "bad!name", "x" * 33])
def test_register_rejects_bad_usernames(service, bad):
    with pytest.raises(InvalidUsernameError):
        service.register(bad, GOOD_PASSWORD)


@pytest.mark.parametrize("weak", ["short1", "allletters", "12345678", "a" * 129])
def test_register_rejects_weak_passwords(service, weak):
    with pytest.raises(WeakPasswordError):
        service.register("alice", weak)


def test_password_is_never_stored_in_plaintext(service, db_path):
    service.register("alice", GOOD_PASSWORD)
    row = sqlite3.connect(db_path).execute("SELECT password_hash FROM users").fetchone()
    assert GOOD_PASSWORD not in row[0]
    assert row[0].startswith("scrypt$")


# ---------- login ----------

def test_login_success(service):
    service.register("alice", GOOD_PASSWORD)
    assert service.login("Alice", GOOD_PASSWORD).username == "alice"


def test_wrong_password_and_unknown_user_look_identical(service):
    service.register("alice", GOOD_PASSWORD)
    with pytest.raises(InvalidCredentialsError) as wrong_password:
        service.login("alice", "not-the-password-1")
    with pytest.raises(InvalidCredentialsError) as unknown_user:
        service.login("nobody", GOOD_PASSWORD)
    assert str(wrong_password.value) == str(unknown_user.value)


# ---------- lockout ----------

def test_account_locks_after_too_many_failures_then_recovers(service, clock):
    service.register("alice", GOOD_PASSWORD)
    for _ in range(MAX_FAILED_ATTEMPTS):
        with pytest.raises(InvalidCredentialsError):
            service.login("alice", "not-the-password-1")

    with pytest.raises(AccountLockedError) as locked:
        service.login("alice", GOOD_PASSWORD)  # even the right password is refused
    assert 0 < locked.value.retry_after <= LOCKOUT_SECONDS + 1

    clock.now += LOCKOUT_SECONDS + 1
    assert service.login("alice", GOOD_PASSWORD).username == "alice"


def test_successful_login_resets_failure_counter(service):
    service.register("alice", GOOD_PASSWORD)
    for _ in range(MAX_FAILED_ATTEMPTS - 1):
        with pytest.raises(InvalidCredentialsError):
            service.login("alice", "not-the-password-1")
    service.login("alice", GOOD_PASSWORD)
    for _ in range(MAX_FAILED_ATTEMPTS - 1):
        with pytest.raises(InvalidCredentialsError):
            service.login("alice", "not-the-password-1")
    assert service.login("alice", GOOD_PASSWORD).username == "alice"
