"""Create deterministic allowlisted directory snapshots.

Version history:
- 1.1.0 (2026-08-28): Caps selection at MAX_SNAPSHOT_ITEMS (2000) by trade count before profile/curve work, fixing a real export rejection (8399 items > 2000 contract limit) that was blocking every hosted publish attempt.
- 1.0.0 (2026-08-23): Deterministic envelope and CLI exporter.
"""
from __future__ import annotations
import argparse, json, uuid
from datetime import datetime, timezone
from pathlib import Path

from app.config import get_settings
from app.contracts import MAX_SNAPSHOT_ITEMS, Snapshot, Strategy, snapshot_hash
from app.repository import local_equity_curves, local_strategies
from app.intelligence.profile import build_profile


def build_snapshot(items, source_watermark: str | datetime, generated_at: datetime | None = None,profiles=None,return_series=None) -> Snapshot:
    records = sorted([x if isinstance(x, Strategy) else Strategy.model_validate(x) for x in items], key=lambda x: x.strategy_id)
    when = generated_at or datetime.now(timezone.utc)
    if isinstance(source_watermark,datetime):watermark=source_watermark
    else:
        try:watermark=datetime.fromisoformat(source_watermark.replace("Z","+00:00"))
        except ValueError:watermark=datetime.strptime(source_watermark,"%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)
    if watermark.tzinfo is None:raise ValueError("source watermark must include a timezone")
    watermark=watermark.astimezone(timezone.utc)
    profiles=list(profiles or []);return_series=list(return_series or []);digest = snapshot_hash(records,profiles,return_series)
    return Snapshot(snapshot_id=f"dna-{watermark.strftime('%Y%m%dT%H%M%SZ')}-{digest[:12]}", source_watermark=watermark,
                    generated_at=when, item_count=len(records), sha256=digest, items=records,intelligence_profiles=profiles,return_series=return_series)


def main():
    parser = argparse.ArgumentParser(); parser.add_argument("--output", required=True); parser.add_argument("--watermark")
    args = parser.parse_args(); watermark = args.watermark or datetime.now(timezone.utc).isoformat()
    settings=get_settings();items=local_strategies(settings)
    # local_strategies() now also attaches open_trades/open_net_return (live
    # local-only fields, see app/repository.py). Strip them before publish:
    # the currently-deployed hosted server doesn't have those fields on its
    # Strategy contract yet, so including them changes this snapshot's
    # sha256 in a way the server's own reconciliation can't reproduce,
    # causing every finalize() to fail with a hash-mismatch 422. Remove this
    # once the open-trade contract change (commit 1453f83f) is confirmed
    # deployed hosted - see agent board topic ep051-hosted-publish.
    for item in items:
        item.pop("open_trades", None)
        item.pop("open_net_return", None)
    # The Snapshot contract caps a publish at MAX_SNAPSHOT_ITEMS. Select the
    # busiest strategies by trade count deterministically (same ordering
    # convention as sync.warm_local_intelligence) rather than truncating in
    # whatever order the database happens to return rows.
    items.sort(key=lambda item:(-item["total_trades"],item["strategy_id"]))
    items=items[:MAX_SNAPSHOT_ITEMS]
    selected_ids={item["strategy_id"] for item in items}
    curves={strategy_id:points for strategy_id,points in local_equity_curves(settings).items() if strategy_id in selected_ids}
    profiles=[build_profile(item,curves.get(item["strategy_id"],[])) for item in items];series=[]
    for strategy_id,points in curves.items():
        for point in points:series.append({"strategy_id":strategy_id,"trade_id":str(point.get("guid") or point["trade_number"]),"trade_number":point["trade_number"],"opened_at":point.get("opened_at"),"observed_at":point["closed_at"],"net_return":point["net_return"],"cumulative_net_return":point["equity"],"drawdown":point["drawdown"],"product":point.get("product"),"signal":point.get("signal"),"entry_price":point.get("entry_price"),"exit_price":point.get("exit_price")})
    snapshot = build_snapshot(items,watermark,profiles=profiles,return_series=series)
    target = Path(args.output); target.write_text(snapshot.model_dump_json(indent=2), encoding="utf-8")
    print(json.dumps({"snapshot_id": snapshot.snapshot_id, "items": snapshot.item_count, "sha256": snapshot.sha256}))


if __name__ == "__main__": main()
