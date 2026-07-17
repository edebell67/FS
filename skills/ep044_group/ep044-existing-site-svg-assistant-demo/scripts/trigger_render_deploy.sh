#!/usr/bin/env bash
# Trigger a deployment of the existing shared Render assistant service.
# Required: RENDER_API_KEY must be available in the process environment.
# Never put the key in this file, Git, command history, or chat.
set -euo pipefail

SERVICE_ID="${1:-${RENDER_SERVICE_ID:-srv-d9b1v06q1p3s73emngn0}}"
: "${RENDER_API_KEY:?Set RENDER_API_KEY in the Hermes environment before running this script.}"

response_file="$(mktemp)"
trap 'rm -f "$response_file"' EXIT

http_code="$(curl --silent --show-error --output "$response_file" --write-out '%{http_code}' \
  --request POST \
  --header "Authorization: Bearer ${RENDER_API_KEY}" \
  --header 'Accept: application/json' \
  "https://api.render.com/v1/services/${SERVICE_ID}/deploys")"

if [[ "$http_code" != "201" && "$http_code" != "200" ]]; then
  echo "Render deploy trigger failed (HTTP ${http_code})." >&2
  python3 - "$response_file" <<'PY' >&2
from pathlib import Path
print(Path(__import__('sys').argv[1]).read_text(errors='replace'))
PY
  exit 1
fi

python3 - "$response_file" "$SERVICE_ID" <<'PY'
import json, sys
from pathlib import Path
payload = json.loads(Path(sys.argv[1]).read_text())
print(f"deploy_triggered=true service={sys.argv[2]}")
print(f"deploy_id={payload.get('id', 'unknown')}")
print(f"status={payload.get('status', 'unknown')}")
PY
