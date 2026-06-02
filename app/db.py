import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_PATH = Path(os.getenv("APP_DB_PATH", "test_app.db"))

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    role TEXT NOT NULL DEFAULT 'user',
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

SEED_USERS = [
    ("Asha QA", "asha.qa@example.com", "qa_engineer"),
    ("Lavan SDET", "lavan.sdet@example.com", "automation_engineer"),
]


@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db(seed: bool = True) -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True) if DB_PATH.parent != Path(".") else None
    with get_connection() as conn:
        conn.executescript(SCHEMA)
        if seed:
            for name, email, role in SEED_USERS:
                conn.execute(
                    "INSERT OR IGNORE INTO users(name, email, role) VALUES (?, ?, ?)",
                    (name, email, role),
                )
        conn.commit()


def reset_db() -> None:
    if DB_PATH.exists():
        DB_PATH.unlink()
    init_db(seed=True)


def fetch_users() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, name, email, role, is_active FROM users ORDER BY id"
        ).fetchall()
        return [dict(row) for row in rows]


def fetch_user_by_email(email: str) -> dict | None:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, name, email, role, is_active FROM users WHERE email = ?",
            (email,),
        ).fetchone()
        return dict(row) if row else None


def create_user(name: str, email: str, role: str) -> dict:
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO users(name, email, role) VALUES (?, ?, ?)",
            (name, email, role),
        )
        conn.commit()
        return {
            "id": cursor.lastrowid,
            "name": name,
            "email": email,
            "role": role,
            "is_active": True,
        }
