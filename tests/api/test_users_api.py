import logging

import pytest
from pydantic import TypeAdapter

from app.schemas import UserResponse

logger = logging.getLogger(__name__)


@pytest.mark.api
@pytest.mark.smoke
def test_health_check_returns_ok(api_client):
    response = api_client.get(f"{api_client.base_url}/api/health", timeout=5)
    logger.info("Health response: %s", response.json())

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.api
@pytest.mark.regression
def test_get_users_matches_response_schema(api_client):
    response = api_client.get(f"{api_client.base_url}/api/users", timeout=5)

    assert response.status_code == 200
    users = TypeAdapter(list[UserResponse]).validate_python(response.json())
    assert len(users) >= 2
    assert all(user.email for user in users)


@pytest.mark.api
@pytest.mark.critical
@pytest.mark.flaky(reruns=1)
def test_create_user_and_fetch_by_email(api_client, unique_user_payload):
    create_response = api_client.post(
        f"{api_client.base_url}/api/users",
        json=unique_user_payload,
        timeout=5,
    )
    assert create_response.status_code == 201
    created_user = UserResponse.model_validate(create_response.json())
    assert created_user.email == unique_user_payload["email"]

    fetch_response = api_client.get(
        f"{api_client.base_url}/api/users/{created_user.email}",
        timeout=5,
    )
    assert fetch_response.status_code == 200
    fetched_user = UserResponse.model_validate(fetch_response.json())
    assert fetched_user.id == created_user.id


@pytest.mark.api
@pytest.mark.regression
def test_duplicate_email_returns_conflict(api_client, unique_user_payload):
    first_response = api_client.post(f"{api_client.base_url}/api/users", json=unique_user_payload)
    second_response = api_client.post(f"{api_client.base_url}/api/users", json=unique_user_payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert second_response.json()["detail"] == "Email already exists"
