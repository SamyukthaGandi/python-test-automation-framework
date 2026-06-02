import sqlite3

import pytest


@pytest.mark.db
@pytest.mark.smoke
def test_users_table_exists(db_path, base_url):
    with sqlite3.connect(db_path) as conn:
        table = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
        ).fetchone()
    assert table is not None


@pytest.mark.db
@pytest.mark.regression
def test_seed_users_are_available(db_path, base_url):
    with sqlite3.connect(db_path) as conn:
        count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        automation_user = conn.execute(
            "SELECT email FROM users WHERE email = ?",
            ("lavan.sdet@example.com",),
        ).fetchone()

    assert count >= 2
    assert automation_user is not None


@pytest.mark.db
@pytest.mark.critical
def test_api_created_user_is_persisted_in_database(api_client, unique_user_payload, db_path):
    response = api_client.post(f"{api_client.base_url}/api/users", json=unique_user_payload)
    assert response.status_code == 201

    with sqlite3.connect(db_path) as conn:
        row = conn.execute(
            "SELECT name, email, role FROM users WHERE email = ?",
            (unique_user_payload["email"],),
        ).fetchone()

    assert row is not None
    assert row[0] == unique_user_payload["name"]
    assert row[2] == unique_user_payload["role"]
