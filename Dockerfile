FROM mcr.microsoft.com/playwright/python:v1.49.1-noble

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app
ENV APP_DB_PATH=/app/test_app.db

CMD ["pytest", "-n", "auto", "--reruns", "1", "--reruns-delay", "1", "--html=reports/pytest_report.html", "--self-contained-html"]
