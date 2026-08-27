"""Validate and emit the deterministic EP051 migration plan. Version 1.0.0."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DB = Path(__file__).resolve().parent

def plan() -> list[dict[str, str]]:
    lines = (DB / "migrations" / "manifest.txt").read_text(encoding="utf-8").splitlines()
    items = []
    for line in lines:
        rel = line.strip()
        if not rel or rel.startswith("#"):
            continue
        target = (ROOT / rel).resolve()
        if ROOT not in target.parents or not target.is_file():
            raise ValueError(f"invalid migration path: {rel}")
        payload = target.read_bytes()
        if not payload.strip():
            raise ValueError(f"empty migration: {rel}")
        items.append({"id": rel, "sha256": hashlib.sha256(payload).hexdigest()})
    ids = [item["id"] for item in items]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate migration id")
    return items

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = plan()
    print(json.dumps(result, indent=2) if args.json else f"validated {len(result)} ordered migrations")
