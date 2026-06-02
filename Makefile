.PHONY: install browsers app test smoke api ui db docker clean

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

browsers:
	python -m playwright install chromium

app:
	uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

test:
	pytest -n auto --reruns 1 --reruns-delay 1

smoke:
	pytest -m smoke

api:
	pytest tests/api -m api

ui:
	pytest tests/ui -m ui

db:
	pytest tests/database -m db

docker:
	docker compose up --build --abort-on-container-exit

clean:
	rm -rf .pytest_cache reports/* test_app.db htmlcov .coverage
	touch reports/.gitkeep
