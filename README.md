# Python Test Automation Framework with CI/CD

Python SDET automation framework that tests a real sample application across API, UI, and database layers.

## What This Framework Demonstrates

- API automation using `requests`
- UI automation using `Playwright`
- Database validation using `SQLite`
- PyTest fixtures and reusable test setup
- PyTest markers for smoke, regression, API, UI, DB, and critical tests
- Retry logic for flaky tests using `pytest-rerunfailures`
- Pydantic schema validation for API response contracts
- Logging to console and file
- Screenshot capture on UI failures
- HTML test reports using `pytest-html`
- Allure result generation support
- Parallel execution using `pytest-xdist`
- Dockerized test execution
- GitHub Actions CI/CD pipeline with report artifacts

## Architecture

```text
python-test-automation-framework/
├── app/                         # Sample FastAPI application under test
│   ├── main.py                   # API routes and demo UI page
│   ├── db.py                     # SQLite database helpers
│   └── schemas.py                # Pydantic request/response schemas
├── tests/
│   ├── conftest.py               # Fixtures, app startup, logging, screenshot hook
│   ├── api/                      # API tests
│   ├── ui/                       # Playwright UI tests
│   └── database/                 # DB validation tests
├── reports/                      # HTML reports, logs, screenshots, allure results
├── scripts/run_tests.sh          # One-command local test runner
├── .github/workflows/ci.yml      # GitHub Actions CI/CD pipeline
├── Dockerfile                    # Dockerized test runner
├── docker-compose.yml            # Docker Compose execution
├── Makefile                      # Common commands
├── requirements.txt              # Python dependencies
└── pyproject.toml                # PyTest config and project metadata
```

## Tech Stack

| Area | Tool |
|---|---|
| Language | Python 3.11+ |
| Test Framework | PyTest |
| API Testing | Requests |
| UI Testing | Playwright |
| DB Validation | SQLite |
| Schema Validation | Pydantic |
| Reporting | PyTest HTML, Allure results |
| Parallel Execution | PyTest xdist |
| Retry Logic | PyTest rerunfailures |
| CI/CD | GitHub Actions |
| Containerization | Docker, Docker Compose |
| Sample App | FastAPI |

## Prerequisites

Install these before running locally:

- Python 3.11 or higher
- Git
- Docker Desktop, optional but recommended

## Local Setup

### 1. Clone the repo

```bash
git clone https://github.com/SamyukthaGandi/python-test-automation-framework.git
cd python-test-automation-framework
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Install Playwright browser

```bash
python -m playwright install chromium
```

## Run the Sample Application Manually

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open:

```text
http://127.0.0.1:8000
```

API health endpoint:

```text
http://127.0.0.1:8000/api/health
```

## Run Tests

Run full framework:

```bash
pytest
```

Run in parallel with retry:

```bash
pytest -n auto --reruns 1 --reruns-delay 1
```

Run smoke tests:

```bash
pytest -m smoke
```

Run API tests:

```bash
pytest tests/api -m api
```

Run UI tests:

```bash
pytest tests/ui -m ui
```

Run DB tests:

```bash
pytest tests/database -m db
```

Run critical release checks:

```bash
pytest -m critical
```

## Reports and Artifacts

After execution, check:

```text
reports/pytest_report.html
reports/test_run.log
reports/framework.log
reports/screenshots/
reports/allure-results/
```

UI failure screenshots are automatically captured under:

```text
reports/screenshots/
```

## Docker Execution

Build and run tests in Docker:

```bash
docker compose up --build --abort-on-container-exit
```

Or directly:

```bash
docker build -t python-sdet-framework .
docker run --rm -v ${PWD}/reports:/app/reports python-sdet-framework
```

Windows PowerShell Docker command:

```powershell
docker run --rm -v ${PWD}/reports:/app/reports python-sdet-framework
```

## GitHub Actions CI/CD

The pipeline runs on:

- Push to `main` or `master`
- Pull request to `main` or `master`
- Manual workflow dispatch

Pipeline stages:

1. Checkout code
2. Set up Python
3. Install dependencies
4. Install Playwright Chromium
5. Run smoke tests
6. Run full regression suite in parallel
7. Upload reports and screenshots as GitHub Actions artifacts
8. Build Docker image
9. Run test suite inside Docker
10. Upload Docker execution reports
