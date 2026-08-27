"""Environment template validation. Version 1.0.0 (2026-08-23)."""
from pathlib import Path
root=Path(__file__).parents[2];text=(root/"deploy"/".env.example").read_text(encoding="utf-8")
entries=dict(line.split("=",1) for line in text.splitlines() if line and not line.startswith("#"))
assert entries["EP051_BROKER_PROFILE"]=="disabled"
assert entries["EP051_DB_PASSWORD"].startswith("__REQUIRED_SECRET_")
assert not any(marker in text.lower() for marker in ("api_key=sk-","bearer ey","password=postgres","broker_token="))
assert set(entries)>={"EP051_ENVIRONMENT","EP051_HTTP_PORT","EP051_DB_NAME","EP051_DB_USER","EP051_DB_PASSWORD","EP051_SNAPSHOT"}
print("environment template and secret boundary validation passed")

