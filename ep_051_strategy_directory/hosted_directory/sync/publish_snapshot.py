"""Outbound-only idempotent snapshot publisher.

Version history:
- 1.0.0 (2026-08-23): Bounded retry and idempotency support.
"""
from __future__ import annotations
import argparse, time
from pathlib import Path
import httpx
from app.contracts import Snapshot


def publish_snapshot(snapshot: Snapshot, url: str, token: str, transport=None, attempts: int = 4):
    snapshot.verified(); delay = .25
    with httpx.Client(timeout=20, transport=transport) as client:
        for attempt in range(attempts):
            try:
                response = client.post(url.rstrip("/") + "/internal/snapshots", content=snapshot.model_dump_json(),
                    headers={"Authorization": f"Bearer {token}", "Idempotency-Key": snapshot.snapshot_id,
                             "Content-Type": "application/json"})
                if response.status_code < 500:
                    response.raise_for_status(); return response.json()
            except httpx.TransportError:
                if attempt == attempts - 1: raise
            time.sleep(delay); delay = min(delay * 2, 2)
    raise RuntimeError("snapshot publication exhausted retries")


def main():
    parser=argparse.ArgumentParser(); parser.add_argument("snapshot"); parser.add_argument("--url",required=True); parser.add_argument("--token",required=True)
    args=parser.parse_args(); snap=Snapshot.model_validate_json(Path(args.snapshot).read_text(encoding="utf-8"))
    print(publish_snapshot(snap,args.url,args.token))


if __name__ == "__main__": main()
