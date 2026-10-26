"""Data models for the auth module."""

from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    id: int
    username: str
    password_hash: str
    created_at: str
    failed_attempts: int = 0
    locked_until: float = 0.0
