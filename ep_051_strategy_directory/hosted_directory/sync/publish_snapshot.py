"""Outbound-only idempotent snapshot publisher.

Version history:
- 2.0.0 (2026-08-28): Replaces the single large POST /internal/snapshots
  request (whole ~28MB/2000-strategy body in one call) with the staged,
  batched ingestion path (PUB-04): POST .../begin (envelope only), then N
  small POST .../batch calls (default 125 strategies per batch, chunked
  by strategy_id order so return_series/profiles for a strategy always
  travel with its item row), then POST .../finalize, which is where the
  server reassembles and verifies the full snapshot exactly as promote()
  always did. CLI signature (snapshot path, --url, --token) is unchanged,
  so deploy/sync_to_hosted.ps1 needed no changes. Each call carries its own
  Idempotency-Key so a retried begin/batch/finalize never double-applies.
- 1.0.0 (2026-08-23): Bounded retry and idempotency support.
"""
from __future__ import annotations
import argparse, time
from pathlib import Path
import httpx
from app.contracts import Snapshot, SnapshotBatch

DEFAULT_BATCH_SIZE = 125


def _post(client: httpx.Client, url: str, token: str, idempotency_key: str, body: str, attempts: int = 4):
    delay = .25
    for attempt in range(attempts):
        try:
            response = client.post(url, content=body,
                headers={"Authorization": f"Bearer {token}", "Idempotency-Key": idempotency_key,
                         "Content-Type": "application/json"})
            if response.status_code < 500:
                response.raise_for_status(); return response.json()
        except httpx.TransportError:
            if attempt == attempts - 1: raise
        time.sleep(delay); delay = min(delay * 2, 2)
    raise RuntimeError(f"request to {url} exhausted retries")


def publish_snapshot(snapshot: Snapshot, url: str, token: str, transport=None, attempts: int = 4, batch_size: int = DEFAULT_BATCH_SIZE):
    snapshot.verified()
    base = url.rstrip("/") + f"/internal/snapshots/{snapshot.snapshot_id}"
    ordered_items = sorted(snapshot.items, key=lambda item: item.strategy_id)
    profiles_by_strategy = {profile.identity.strategy_id: profile for profile in snapshot.intelligence_profiles}
    series_by_strategy: dict[str, list] = {}
    for point in snapshot.return_series:
        series_by_strategy.setdefault(point.strategy_id, []).append(point)

    with httpx.Client(timeout=20, transport=transport) as client:
        envelope = snapshot.model_dump_json(include={"schema_version", "methodology_version", "snapshot_id",
            "source_watermark", "generated_at", "item_count", "sha256"})
        _post(client, base + "/begin", token, snapshot.snapshot_id, envelope, attempts)

        result = None
        for batch_index, start in enumerate(range(0, len(ordered_items), batch_size)):
            chunk = ordered_items[start:start + batch_size]
            batch_profiles = [profiles_by_strategy[item.strategy_id] for item in chunk if item.strategy_id in profiles_by_strategy]
            batch_series = [point for item in chunk for point in series_by_strategy.get(item.strategy_id, [])]
            body = SnapshotBatch(batch_index=batch_index, items=chunk, intelligence_profiles=batch_profiles, return_series=batch_series).model_dump_json()
            result = _post(client, base + "/batch", token, f"{snapshot.snapshot_id}:{batch_index}", body, attempts)

        result = _post(client, base + "/finalize", token, snapshot.snapshot_id, "", attempts)
        return result


def main():
    parser=argparse.ArgumentParser(); parser.add_argument("snapshot"); parser.add_argument("--url",required=True); parser.add_argument("--token",required=True)
    parser.add_argument("--batch-size",type=int,default=DEFAULT_BATCH_SIZE)
    args=parser.parse_args(); snap=Snapshot.model_validate_json(Path(args.snapshot).read_text(encoding="utf-8"))
    print(publish_snapshot(snap,args.url,args.token,batch_size=args.batch_size))


if __name__ == "__main__": main()
