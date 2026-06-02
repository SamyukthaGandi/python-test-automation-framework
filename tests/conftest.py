import logging
import os
import socket
import subprocess
import sys
import time
from pathlib import Path
from typing import Iterator

import pytest
import requests
from playwright.sync_api import Page

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = PROJECT_ROOT / "reports"
SCREENSHOTS_DIR = REPORTS_DIR / "screenshots"
DB_PATH = PROJECT_ROOT / f"test_app_{os.environ.get('PYTEST_XDIST_WORKER', 'local')}.db"


def pytest_configure(config):
    REPORTS_DIR.mkdir(exist_ok=True)
    SCREENSHOTS_DIR.mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler(REPORTS_DIR / "framework.log"),
            logging.StreamHandler(),
        ],
    )


def _get_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


@pytest.fixture(scope="session")
def base_url() -> Iterator[str]:
    """Start the sample FastAPI app once for API and UI tests."""
    port = _get_free_port()
    url = f"http://127.0.0.1:{port}"
    env = os.environ.copy()
    env["APP_DB_PATH"] = str(DB_PATH)
    env["PYTHONPATH"] = str(PROJECT_ROOT)

    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", str(port)],
        cwd=PROJECT_ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    deadline = time.time() + 30
    while time.time() < deadline:
        try:
            response = requests.get(f"{url}/api/health", timeout=1)
            if response.status_code == 200:
                break
        except requests.RequestException:
            time.sleep(0.5)
    else:
        output = process.stdout.read() if process.stdout else "No process output"
        process.terminate()
        raise RuntimeError(f"Sample app did not start. Output:\n{output}")

    yield url
    process.terminate()
    process.wait(timeout=10)


@pytest.fixture(scope="session")
def api_client(base_url: str) -> requests.Session:
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    session.base_url = base_url  # type: ignore[attr-defined]
    return session


@pytest.fixture()
def unique_user_payload() -> dict:
    timestamp = int(time.time() * 1000)
    return {
        "name": f"Automation User {timestamp}",
        "email": f"automation.user.{timestamp}@example.com",
        "role": "sdet",
    }


@pytest.fixture()
def db_path() -> Path:
    return DB_PATH


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    page: Page | None = item.funcargs.get("page") if hasattr(item, "funcargs") else None

    if report.when == "call" and report.failed and page:
        SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
        screenshot_path = SCREENSHOTS_DIR / f"{item.name}.png"
        page.screenshot(path=str(screenshot_path), full_page=True)
        logging.getLogger(__name__).error("UI failure screenshot saved: %s", screenshot_path)
