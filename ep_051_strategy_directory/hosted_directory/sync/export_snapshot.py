"""Create deterministic allowlisted directory snapshots.

Version history:
- 1.0.0 (2026-08-23): Deterministic envelope and CLI exporter.
"""
from __future__ import annotations
import argparse, json, uuid
from bisect import bisect_right
from datetime import datetime, timezone
from pathlib import Path

from app.config import get_settings
from app.contracts import Snapshot, Strategy, snapshot_hash, MAX_SNAPSHOT_ITEMS
from app.repository import local_equity_curves, local_strategies
from app.intelligence.profile import build_profile


def select_snapshot_items(items) -> list[Strategy]:
    """Select the stable contract-bounded strategy population before curve work."""
    records = sorted((item if isinstance(item, Strategy) else Strategy.model_validate(item) for item in items), key=lambda item: item.strategy_id)
    return records[:MAX_SNAPSHOT_ITEMS]


def _rank_at_each_point(curves):
    timelines={sid:([p["closed_at"] for p in points],[p["equity"] for p in points]) for sid,points in curves.items()}
    total=len(timelines); ranks={}
    for strategy_id,points in curves.items():
        result=[]
        for point in points:
            higher=0
            for times,values in timelines.values():
                position=bisect_right(times,point["closed_at"])-1
                if position>=0 and values[position]>point["equity"]:higher+=1
            result.append((higher+1,total))
        ranks[strategy_id]=result
    return ranks


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
    settings=get_settings();selected=select_snapshot_items(local_strategies(settings));items=[item.model_dump() for item in selected];curves=local_equity_curves(settings,[item.strategy_id for item in selected])
    profiles=[build_profile(item,curves.get(item["strategy_id"],[])) for item in items];series=[];ranks=_rank_at_each_point(curves)
    for strategy_id,points in curves.items():
        for point,(rank_position,total_strategies) in zip(points,ranks[strategy_id]):series.append({"strategy_id":strategy_id,"trade_id":str(point.get("guid") or point["trade_number"]),"trade_number":point["trade_number"],"opened_at":point.get("opened_at"),"observed_at":point["closed_at"],"net_return":point["net_return"],"cumulative_net_return":point["equity"],"drawdown":point["drawdown"],"product":point.get("product"),"signal":point.get("signal"),"entry_price":point.get("entry_price"),"exit_price":point.get("exit_price"),"alt_net_return":point.get("alt_net_return"),"rank_position":rank_position,"total_strategies":total_strategies})
    snapshot = build_snapshot(items,watermark,profiles=profiles,return_series=series)
    target = Path(args.output); target.write_text(snapshot.model_dump_json(indent=2), encoding="utf-8")
    print(json.dumps({"snapshot_id": snapshot.snapshot_id, "items": snapshot.item_count, "sha256": snapshot.sha256}))


if __name__ == "__main__": main()
