import re

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.ui
@pytest.mark.smoke
def test_home_page_loads(page: Page, base_url: str):
    page.goto(base_url)
    expect(page).to_have_title(re.compile("SDET Demo App"))
    expect(page.get_by_test_id("service-status")).to_have_text("Service is running")


@pytest.mark.ui
@pytest.mark.critical
def test_create_user_from_ui(page: Page, base_url: str, unique_user_payload: dict):
    page.goto(base_url)
    page.get_by_test_id("name-input").fill(unique_user_payload["name"])
    page.get_by_test_id("email-input").fill(unique_user_payload["email"])
    page.get_by_test_id("role-input").fill(unique_user_payload["role"])
    page.get_by_test_id("create-user-button").click()

    expect(page.get_by_test_id("message")).to_have_text("User created successfully")
    expect(page.get_by_test_id("users-table")).to_contain_text(unique_user_payload["email"])
