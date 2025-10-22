#!/usr/bin/env bash
set -euo pipefail
TENANT=${1:-cliente_a}
export ENV_FILE="tenants/${TENANT}.env"
# PERMITE override de PROMPTS_FILE desde el .env del tenant
export PROMPTS_FILE="$(grep -E '^PROMPTS_FILE=' "${ENV_FILE}" | cut -d'=' -f2- || true)"
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000