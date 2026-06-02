#!/usr/bin/env bash
set -euo pipefail

mkdir -p reports/screenshots reports/allure-results

echo "Running API + DB + UI tests in parallel with retry and HTML reporting..."
pytest -n auto --reruns 1 --reruns-delay 1 "$@"
