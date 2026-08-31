"""Create deterministic allowlisted directory snapshots.

Version history:
- 1.3.0 (2026-08-31): Adds alt_net_return, rank_position, and
  total_strategies to every return_series point, closing the gap where
  hosted's trade ledger showed "ALT NET RETURN" and "Position after
  close" columns that local's did (the fields existed in local's own
  live API responses, but were either never selected in
  local_equity_curves()'s SQL - alt_net_return - or had no export/hosted
  read path at all - rank_position/total_strategies, which local computes
  live per-request via /rank-journey, something hosted has no SQL Server
  connection to do). rank_position/total_strategies is necessarily an
  all-time ranking computed once here over the exported/selected
  population (see _rank_at_each_point()), not local's current-day-scoped
  live one - the closest hosted can get without per-request recomputation
  capability it doesn't have.
- 1.2.0 (2026-08-31): Derives every item's trade stats (total_trades, wins/
  losses/breakevens, total_net_return, win_rate, profit_factor, evidence_
  start/end) directly from the same local_equity_curves() read used to
  build return_series, instead of from a separate local_strategies()
  aggregate query. The two queries are independent, non-atomic reads
  against a live table - trades close between them under real load, so
  the counts could (and, under tonight's slower-than-usual export timing,
  reliably did) disagree, failing Snapshot.verified()'s reconciliation on
  every single publish attempt. Selection ranking is now also based on
  the curves read's own trade counts, not the separate aggregate query,
  so selection and stats can never disagree with each other by
  construction. local_strategies() is only used for name/product/market/
  status labels now, which don't need to be transactionally consistent
  with trade counts.
- 1.1.0 (2026-08-28): Caps selection at MAX_SNAPSHOT_ITEMS (2000) by trade count before profile/curve work, fixing a real export rejection (8399 items > 2000 contract limit) that was blocking every hosted publish attempt.
- 1.0.0 (2026-08-23): Deterministic envelope and CLI exporter.
"""
from __future__ import annotations
import argparse, json, uuid
from bisect import bisect_right
from datetime import datetime, timezone
from pathlib import Path

from app.config import get_settings
from app.contracts import MAX_SNAPSHOT_ITEMS, Snapshot, Strategy, snapshot_hash
from app.repository import local_equity_curves, local_strategies
from app.intelligence.profile import build_profile


def _stats_from_points(points):
    """Recompute one strategy's aggregate stats from its own return-series
    points - the same points that get published as return_series - so the
    two can never disagree. Sort order matches Snapshot.verified()'s own
    (observed_at, trade_id) so accumulated floating-point sums land the
    same way (well within its abs_tol=1e-6 either way)."""
    ordered = sorted(points, key=lambda p: (p["closed_at"], p.get("guid") or ""))
    wins = losses = breakevens = 0
    gross_profit = gross_loss = total_net_return = 0.0
    for point in ordered:
        value = point["net_return"]; total_net_return += value
        if value > 0: wins += 1; gross_profit += value
        elif value < 0: losses += 1; gross_loss += abs(value)
        else: breakevens += 1
    total = len(ordered)
    return {
        "total_trades": total, "wins": wins, "losses": losses, "breakevens": breakevens,
        "total_net_return": total_net_return,
        "win_rate": wins / total if total else 0.0,
        "profit_factor": (gross_profit / gross_loss) if gross_loss else None,
        "max_drawdown_money": None,
        "evidence_start": min((p.get("opened_at") or p["closed_at"]) for p in ordered) if ordered else None,
        "evidence_end": max(p["closed_at"] for p in ordered) if ordered else None,
    }


def _rank_at_each_point(curves):
    """For every (strategy_id, point) in curves, that strategy's rank among
    every OTHER strategy in curves by cumulative net_return, at the same
    instant - the hosted equivalent of local's live /rank-journey endpoint,
    precomputed once at export time since hosted has no SQL Server to
    compute this per-request. Necessarily an all-time ranking over
    whatever population curves already holds (the exported/selected
    strategies), not local's current-day-scoped one - hosted has no
    per-request date-window recomputation capability either. Returns
    {strategy_id: [(rank_position, total_strategies), ...]} aligned 1:1
    with each strategy's own points list, in the same order."""
    timelines = {sid: ([p["closed_at"] for p in points], [p["equity"] for p in points]) for sid, points in curves.items()}
    total_strategies = len(timelines)
    ranks = {}
    for strategy_id, points in curves.items():
        strategy_ranks = []
        for point in points:
            at = point["closed_at"]; value = point["equity"]
            higher = 0
            for sid, (times, cum) in timelines.items():
                position = bisect_right(times, at) - 1
                if position >= 0 and cum[position] > value:
                    higher += 1
            strategy_ranks.append((higher + 1, total_strategies))
        ranks[strategy_id] = strategy_ranks
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
    settings=get_settings()
    # Names/labels only (descriptive_name/product_name/market/status) - NOT
    # used for trade counts or selection ranking, see version history.
    name_by_id={row["strategy_id"]:row for row in local_strategies(settings)}
    # Single consistent read: every strategy's curve, in one query. Both the
    # selection ranking and every item's stats are derived from this same
    # data, so they can never disagree with each other by construction.
    all_curves=local_equity_curves(settings)
    selected=sorted(all_curves.items(),key=lambda kv:(-len(kv[1]),kv[0]))[:MAX_SNAPSHOT_ITEMS]
    items=[]
    for strategy_id,points in selected:
        stats=_stats_from_points(points);base=name_by_id.get(strategy_id,{})
        items.append({
            "strategy_id":strategy_id,"descriptive_name":base.get("descriptive_name"),
            "product_name":base.get("product_name"),"market":base.get("market","FX"),
            "status":base.get("status","active"),
            "quality_state":"VALID" if stats["total_trades"]>=30 else "COLLECTING",
            **stats,
        })
    curves=dict(selected)
    profiles=[build_profile(item,curves.get(item["strategy_id"],[])) for item in items];series=[]
    ranks=_rank_at_each_point(curves)
    for strategy_id,points in curves.items():
        strategy_ranks=ranks[strategy_id]
        for point,(rank_position,total_strategies) in zip(points,strategy_ranks):
            series.append({"strategy_id":strategy_id,"trade_id":str(point.get("guid") or point["trade_number"]),"trade_number":point["trade_number"],"opened_at":point.get("opened_at"),"observed_at":point["closed_at"],"net_return":point["net_return"],"cumulative_net_return":point["equity"],"drawdown":point["drawdown"],"product":point.get("product"),"signal":point.get("signal"),"entry_price":point.get("entry_price"),"exit_price":point.get("exit_price"),"alt_net_return":point.get("alt_net_return"),"rank_position":rank_position,"total_strategies":total_strategies})
    snapshot = build_snapshot(items,watermark,profiles=profiles,return_series=series)
    target = Path(args.output); target.write_text(snapshot.model_dump_json(indent=2), encoding="utf-8")
    print(json.dumps({"snapshot_id": snapshot.snapshot_id, "items": snapshot.item_count, "sha256": snapshot.sha256}))


if __name__ == "__main__": main()
