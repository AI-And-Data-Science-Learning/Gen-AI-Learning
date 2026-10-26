"""SQLite-backed user storage."""

import os
import sqlite3
from contextlib import closing
from datetime import datetime, timezone

from src.auth.models import User

DEFAULT_DB_PATH = os.environ.get("AUTH_DB_PATH", "data/auth.db")

_SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TEXT NOT NULL,
    failed_attempts INTEGER NOT NULL DEFAULT 0,
    locked_until REAL NOT NULL DEFAULT 0
)
"""


class UserStore:
    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        self.db_path = db_path
        parent = os.path.dirname(db_path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with closing(self._connect()) as conn, conn:
            conn.execute(_SCHEMA)

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    @staticmethod
    def _row_to_user(row) -> User:
        return User(
            id=row[0],
            username=row[1],
            password_hash=row[2],
            created_at=row[3],
            failed_attempts=row[4],
            locked_until=row[5],
        )

    def add_user(self, username: str, password_hash: str) -> None:
        """Insert a user. Raises sqlite3.IntegrityError if the username exists."""
        created_at = datetime.now(timezone.utc).isoformat()
        with closing(self._connect()) as conn, conn:
            conn.execute(
                "INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)",
                (username, password_hash, created_at),
            )

    def get_user(self, username: str) -> User | None:
        with closing(self._connect()) as conn:
            row = conn.execute(
                "SELECT id, username, password_hash, created_at, failed_attempts, locked_until "
                "FROM users WHERE username = ?",
                (username,),
            ).fetchone()
        return self._row_to_user(row) if row else None

    def set_login_state(self, user_id: int, failed_attempts: int, locked_until: float) -> None:
        with closing(self._connect()) as conn, conn:
            conn.execute(
                "UPDATE users SET failed_attempts = ?, locked_until = ? WHERE id = ?",
                (failed_attempts, locked_until, user_id),
            )
