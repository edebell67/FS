import argparse
import json
import math
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Iterable, List, Tuple
from paths import BREAKOUT_JSON_ROOT # [V20260510_1955]


DEFAULT_MODE = "live"
DEFAULT_PRODUCT_TYPE = "forex"
DEFAULT_TOP_N = 10
DEFAULT_MAX_LAG = 8
DEFAULT_MIN_POINTS = 8
DEFAULT_GRAIN = "strategy"
DEFAULT_PRODUCT_CANDIDATE_LIMIT = 180
SNAPSHOT_MINUTES = 15


@dataclass
class StrategySeries:
    name: str
    snapshots: List[Tuple[datetime, float]]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze _summary_net.json for leading/lagging and lead-lag correlation relationships."
    )
    parser.add_argument("date", nargs="?", default=datetime.now().strftime("%Y-%m-%d"))
    parser.add_argument("--mode", default=DEFAULT_MODE)
    parser.add_argument("--product-type", default=DEFAULT_PRODUCT_TYPE)
    parser.add_argument("--top-n", type=int, default=DEFAULT_TOP_N)
    parser.add_argument("--max-lag", type=int, default=DEFAULT_MAX_LAG)
    parser.add_argument("--min-points", type=int, default=DEFAULT_MIN_POINTS)
    parser.add_argument("--grain", choices=["strategy", "product"], default=DEFAULT_GRAIN)
    parser.add_argument("--candidate-limit", type=int, default=None)
    return parser.parse_args()


def summary_net_path(base_dir: Path, mode: str, product_type: str, date_str: str) -> Path:
    return base_dir / mode / product_type / date_str / "_summary_net.json"


def output_json_path(base_dir: Path, mode: str, product_type: str, date_str: str, grain: str) -> Path:
    suffix = "_summary_net_lead_lag_analysis.json" if grain == "strategy" else "_summary_net_lead_lag_analysis_product_level.json"
    return base_dir / mode / product_type / date_str / suffix


def output_md_path(base_dir: Path, mode: str, product_type: str, date_str: str, grain: str) -> Path:
    suffix = "_summary_net_lead_lag_analysis.md" if grain == "strategy" else "_summary_net_lead_lag_analysis_product_level.md"
    return base_dir / mode / product_type / date_str / suffix


def load_summary(path: Path) -> Dict:
    return json.loads(path.read_text(encoding="utf-8"))


def product_entity_name(strategy_name: str, product_name: str) -> str:
    return f"{strategy_name} / {product_name}"


def floor_to_snapshot(ts: datetime) -> datetime:
    minute = (ts.minute // SNAPSHOT_MINUTES) * SNAPSHOT_MINUTES
    return ts.replace(minute=minute, second=0, microsecond=0)


def aggregate_strategy_series(summary: Dict) -> Tuple[List[datetime], Dict[str, StrategySeries]]:
    strategies = summary.get("strategies", {})
    timeline_updates: Dict[datetime, List[Tuple[str, str, float]]] = {}

    for strategy_name, products in strategies.items():
        for product_name, points in (products or {}).items():
            if not isinstance(points, list):
                continue
            for point in points:
                t_raw = point.get("t")
                if not t_raw:
                    continue
                try:
                    ts = datetime.fromisoformat(t_raw)
                except ValueError:
                    continue
                timeline_updates.setdefault(ts, []).append(
                    (strategy_name, product_name, float(point.get("net", 0.0)))
                )

    if not timeline_updates:
        return [], {}

    sorted_times = sorted(timeline_updates.keys())
    latest_pair_net: Dict[Tuple[str, str], float] = {}
    totals_by_time: Dict[datetime, Dict[str, float]] = {}

    for ts in sorted_times:
        for strategy_name, product_name, net in timeline_updates[ts]:
            latest_pair_net[(strategy_name, product_name)] = net
        totals: Dict[str, float] = {}
        for (strategy_name, _product_name), net in latest_pair_net.items():
            totals[strategy_name] = totals.get(strategy_name, 0.0) + net
        totals_by_time[ts] = totals

    start_time = floor_to_snapshot(sorted_times[0])
    end_time = floor_to_snapshot(sorted_times[-1])
    aligned_times: List[datetime] = []
    current_time = start_time
    last_seen_totals: Dict[str, float] = {}
    sorted_update_times = iter(sorted_times)
    pending_time = next(sorted_update_times, None)
    series_map: Dict[str, List[Tuple[datetime, float]]] = {}

    while current_time <= end_time:
        while pending_time is not None and pending_time <= current_time:
            last_seen_totals = totals_by_time[pending_time]
            pending_time = next(sorted_update_times, None)
        aligned_times.append(current_time)
        for strategy_name, net in last_seen_totals.items():
            series_map.setdefault(strategy_name, []).append((current_time, round(net, 2)))
        current_time += timedelta(minutes=SNAPSHOT_MINUTES)

    return aligned_times, {
        name: StrategySeries(name=name, snapshots=points) for name, points in series_map.items() if len(points) >= 2
    }


def aggregate_product_series(summary: Dict) -> Tuple[List[datetime], Dict[str, StrategySeries]]:
    strategies = summary.get("strategies", {})
    timeline_updates: Dict[datetime, List[Tuple[str, float]]] = {}

    for strategy_name, products in strategies.items():
        for product_name, points in (products or {}).items():
            if not isinstance(points, list):
                continue
            entity_name = product_entity_name(strategy_name, product_name)
            for point in points:
                t_raw = point.get("t")
                if not t_raw:
                    continue
                try:
                    ts = datetime.fromisoformat(t_raw)
                except ValueError:
                    continue
                timeline_updates.setdefault(ts, []).append((entity_name, float(point.get("net", 0.0))))

    if not timeline_updates:
        return [], {}

    sorted_times = sorted(timeline_updates.keys())
    latest_entity_net: Dict[str, float] = {}
    totals_by_time: Dict[datetime, Dict[str, float]] = {}

    for ts in sorted_times:
        for entity_name, net in timeline_updates[ts]:
            latest_entity_net[entity_name] = net
        totals_by_time[ts] = dict(latest_entity_net)

    start_time = floor_to_snapshot(sorted_times[0])
    end_time = floor_to_snapshot(sorted_times[-1])
    aligned_times: List[datetime] = []
    current_time = start_time
    last_seen_totals: Dict[str, float] = {}
    sorted_update_times = iter(sorted_times)
    pending_time = next(sorted_update_times, None)
    series_map: Dict[str, List[Tuple[datetime, float]]] = {}

    while current_time <= end_time:
        while pending_time is not None and pending_time <= current_time:
            last_seen_totals = totals_by_time[pending_time]
            pending_time = next(sorted_update_times, None)
        aligned_times.append(current_time)
        for entity_name, net in last_seen_totals.items():
            series_map.setdefault(entity_name, []).append((current_time, round(net, 2)))
        current_time += timedelta(minutes=SNAPSHOT_MINUTES)

    return aligned_times, {
        name: StrategySeries(name=name, snapshots=points) for name, points in series_map.items() if len(points) >= 2
    }


def snapshot_nets(series: StrategySeries) -> List[float]:
    return [net for _ts, net in series.snapshots]


def snapshot_deltas(series: StrategySeries) -> List[float]:
    nets = snapshot_nets(series)
    return [round(nets[idx] - nets[idx - 1], 2) for idx in range(1, len(nets))]


def entity_activity(series: StrategySeries) -> Dict[str, float]:
    deltas = snapshot_deltas(series)
    nets = snapshot_nets(series)
    return {
        "total_abs_delta": round(sum(abs(value) for value in deltas), 2),
        "net_change": round(nets[-1] - nets[0], 2) if len(nets) >= 2 else 0.0,
        "snapshot_count": len(nets),
    }


def mean(values: Iterable[float]) -> float:
    values = list(values)
    if not values:
        return 0.0
    return sum(values) / len(values)


def pearson_correlation(x_values: List[float], y_values: List[float]) -> float:
    if len(x_values) != len(y_values) or len(x_values) < 2:
        return 0.0
    mean_x = mean(x_values)
    mean_y = mean(y_values)
    num = sum((x - mean_x) * (y - mean_y) for x, y in zip(x_values, y_values))
    den_x = math.sqrt(sum((x - mean_x) ** 2 for x in x_values))
    den_y = math.sqrt(sum((y - mean_y) ** 2 for y in y_values))
    if den_x == 0 or den_y == 0:
        return 0.0
    return num / (den_x * den_y)


def analyze_pair_lags(
    leader_deltas: List[float],
    follower_deltas: List[float],
    max_lag: int,
    min_points: int,
) -> Dict[str, float] | None:
    best_positive = None
    best_negative = None
    max_test_lag = max(0, min(max_lag, len(leader_deltas) - min_points, len(follower_deltas) - min_points))

    for lag in range(0, max_test_lag + 1):
        if lag == 0:
            lhs = leader_deltas
            rhs = follower_deltas
        else:
            lhs = leader_deltas[:-lag]
            rhs = follower_deltas[lag:]
        if len(lhs) < min_points or len(rhs) < min_points:
            continue
        corr = pearson_correlation(lhs, rhs)
        candidate = {
            "lag_steps": lag,
            "lag_minutes": lag * SNAPSHOT_MINUTES,
            "correlation": round(corr, 4),
            "sample_points": len(lhs),
        }
        if best_positive is None or candidate["correlation"] > best_positive["correlation"]:
            best_positive = candidate
        if best_negative is None or candidate["correlation"] < best_negative["correlation"]:
            best_negative = candidate

    if best_positive is None or best_negative is None:
        return None
    return {
        "best_positive": best_positive,
        "best_negative": best_negative,
    }


def select_analysis_universe(
    series_map: Dict[str, StrategySeries],
    grain: str,
    candidate_limit: int | None,
) -> List[str]:
    scored = []
    for entity_name, series in series_map.items():
        metrics = entity_activity(series)
        scored.append((entity_name, metrics["total_abs_delta"], abs(metrics["net_change"]), metrics["snapshot_count"]))
    scored.sort(key=lambda item: (-item[1], -item[2], -item[3], item[0]))

    if candidate_limit is None:
        candidate_limit = len(scored) if grain == "strategy" else min(DEFAULT_PRODUCT_CANDIDATE_LIMIT, len(scored))

    return [name for name, *_rest in scored[:candidate_limit]]


def build_relationship_rows(
    series_map: Dict[str, StrategySeries],
    candidate_names: List[str],
    max_lag: int,
    min_points: int,
    relationship: str,
) -> List[Dict]:
    rows = []
    for leader_name in candidate_names:
        leader_deltas = snapshot_deltas(series_map[leader_name])
        for lagging_name in candidate_names:
            if leader_name == lagging_name:
                continue
            lagging_deltas = snapshot_deltas(series_map[lagging_name])
            analysis = analyze_pair_lags(
                leader_deltas,
                lagging_deltas,
                max_lag=max_lag,
                min_points=min_points,
            )
            if not analysis:
                continue

            candidate = analysis["best_positive"] if relationship == "positive" else analysis["best_negative"]
            if candidate["lag_steps"] <= 0:
                continue
            if relationship == "positive" and candidate["correlation"] <= 0:
                continue
            if relationship == "inverse" and candidate["correlation"] >= 0:
                continue

            rows.append(
                {
                    "leader_strategy": leader_name,
                    "lagging_strategy": lagging_name,
                    "relationship": relationship,
                    **candidate,
                }
            )

    if relationship == "positive":
        rows.sort(key=lambda item: (-item["correlation"], item["lag_steps"], item["leader_strategy"], item["lagging_strategy"]))
    else:
        rows.sort(key=lambda item: (item["correlation"], item["lag_steps"], item["leader_strategy"], item["lagging_strategy"]))
    return rows


def rank_entities_from_relationships(
    rows: List[Dict],
    role_key: str,
    entity_label: str,
    top_n: int,
) -> List[Dict]:
    aggregates: Dict[str, Dict[str, float]] = {}
    for row in rows:
        entity_name = row[role_key]
        agg = aggregates.setdefault(
            entity_name,
            {
                entity_label: entity_name,
                "relationship_score": 0.0,
                "pair_count": 0,
                "best_correlation": 0.0,
                "weighted_lag_total": 0.0,
                "weight_total": 0.0,
            },
        )
        weight = abs(float(row["correlation"])) * float(row["sample_points"])
        agg["relationship_score"] += weight
        agg["pair_count"] += 1
        if abs(float(row["correlation"])) > abs(float(agg["best_correlation"])):
            agg["best_correlation"] = float(row["correlation"])
        agg["weighted_lag_total"] += float(row["lag_minutes"]) * weight
        agg["weight_total"] += weight

    ranked = []
    for entity_name, agg in aggregates.items():
        weight_total = agg["weight_total"] or 1.0
        ranked.append(
            {
                entity_label: entity_name,
                "relationship_score": round(agg["relationship_score"], 2),
                "pair_count": int(agg["pair_count"]),
                "best_correlation": round(float(agg["best_correlation"]), 4),
                "avg_lag_minutes": round(agg["weighted_lag_total"] / weight_total, 2),
            }
        )

    ranked.sort(key=lambda item: (-item["relationship_score"], -abs(item["best_correlation"]), item[entity_label]))
    return ranked[:top_n]


def build_pair_results(
    series_map: Dict[str, StrategySeries],
    left_names: List[str],
    right_names: List[str],
    max_lag: int,
    min_points: int,
    positive_only: bool = False,
    negative_only: bool = False,
    require_positive_lag: bool = False,
    dedupe_symmetric: bool = False,
) -> List[Dict]:
    rows = []
    seen_pairs = set()
    for left_name in left_names:
        for right_name in right_names:
            if left_name == right_name:
                continue
            if dedupe_symmetric:
                pair_key = tuple(sorted((left_name, right_name)))
                if pair_key in seen_pairs:
                    continue
                seen_pairs.add(pair_key)
            analysis = analyze_pair_lags(
                snapshot_deltas(series_map[left_name]),
                snapshot_deltas(series_map[right_name]),
                max_lag=max_lag,
                min_points=min_points,
            )
            if not analysis:
                continue
            if not negative_only:
                best_positive = analysis["best_positive"]
                if require_positive_lag and best_positive["lag_steps"] <= 0:
                    best_positive = None
                if best_positive is not None:
                    rows.append(
                        {
                            "leader_strategy": left_name,
                            "lagging_strategy": right_name,
                            "relationship": "positive",
                            **best_positive,
                        }
                    )
            if not positive_only:
                best_negative = analysis["best_negative"]
                if require_positive_lag and best_negative["lag_steps"] <= 0:
                    best_negative = None
                if best_negative is not None:
                    rows.append(
                        {
                            "leader_strategy": left_name,
                            "lagging_strategy": right_name,
                            "relationship": "inverse",
                            **best_negative,
                        }
                    )

    if positive_only:
        rows = [row for row in rows if row["correlation"] > 0]
        rows.sort(key=lambda item: (-item["correlation"], item["lag_steps"], item["leader_strategy"], item["lagging_strategy"]))
    elif negative_only:
        rows = [row for row in rows if row["correlation"] < 0]
        rows.sort(key=lambda item: (item["correlation"], item["lag_steps"], item["leader_strategy"], item["lagging_strategy"]))
    return rows


def all_strategy_names(series_map: Dict[str, StrategySeries]) -> List[str]:
    return sorted(series_map.keys())


def build_report(
    date_str: str,
    mode: str,
    product_type: str,
    grain: str,
    summary_path: Path,
    snapshot_count: int,
    universe_size: int,
    leaders: List[Dict],
    laggers: List[Dict],
    lead_lag_pairs: List[Dict],
    inverse_pairs: List[Dict],
    inverse_leaders: List[Dict],
    max_lag: int,
) -> str:
    entity_label = "strategy" if grain == "strategy" else "strategy_product"
    entity_display = "Strategies" if grain == "strategy" else "Strategy/Product Series"
    entity_method = "strategy-level return patterns aggregated across products" if grain == "strategy" else "individual strategy + product return patterns"

    lines = [
        f"# Summary Net Lead/Lag Analysis",
        "",
        f"- Date: `{date_str}`",
        f"- Mode: `{mode}`",
        f"- Product type: `{product_type}`",
        f"- Grain: `{grain}`",
        f"- Source: `{summary_path}`",
        f"- Snapshot interval: `{SNAPSHOT_MINUTES}m`",
        f"- Snapshot count: `{snapshot_count}`",
        f"- Candidate universe: `{universe_size}` entities",
        f"- Max lag tested: `{max_lag * SNAPSHOT_MINUTES}m`",
        "",
        "## Method",
        "",
        f"- `Leading` means the earlier member of a time-shifted relationship in {entity_method}.",
        f"- `Lagging` means the later member of a similar relationship at a consistent positive delay.",
        f"- Analysis uses 15-minute net-change series derived from `_summary_net.json`.",
        "- Positive lead/lag means the lagger follows later with positive correlation.",
        "- Inverse lead/lag means the lagger follows later with negative correlation.",
        "- Leader and lagger rankings are based on accumulated lagged relationship strength, not final PnL rank.",
        "",
        f"## Leading {entity_display}",
        "",
    ]

    for idx, row in enumerate(leaders, start=1):
        lines.append(
            f"{idx}. `{row[entity_label]}` score `{row['relationship_score']:.2f}`, pairs `{row['pair_count']}`, best corr `{row['best_correlation']:+.4f}`, avg lag `{row['avg_lag_minutes']:.1f}m`"
        )

    lines.extend(["", f"## Lagging {entity_display}", ""])
    for idx, row in enumerate(laggers, start=1):
        lines.append(
            f"{idx}. `{row[entity_label]}` score `{row['relationship_score']:.2f}`, pairs `{row['pair_count']}`, best corr `{row['best_correlation']:+.4f}`, avg lag `{row['avg_lag_minutes']:.1f}m`"
        )

    lines.extend(["", f"## Positive Lead/Lag Relationships", ""])
    if lead_lag_pairs:
        for idx, row in enumerate(lead_lag_pairs[:10], start=1):
            lines.append(
                f"{idx}. `{row['leader_strategy']}` -> `{row['lagging_strategy']}` corr `{row['correlation']:+.4f}` at `{row['lag_minutes']}m` lag"
            )
    else:
        lines.append("No positive lead/lag relationships passed the ranking filters.")

    lines.extend(["", "## Inverse Lead/Lag Relationships", ""])
    if inverse_pairs:
        for idx, row in enumerate(inverse_pairs[:10], start=1):
            lines.append(
                f"{idx}. `{row['leader_strategy']}` -> `{row['lagging_strategy']}` corr `{row['correlation']:+.4f}` at `{row['lag_minutes']}m` lag"
            )
    else:
        lines.append("No inverse lead/lag relationships passed the ranking filters.")

    lines.extend(["", f"## Leading {entity_display} Inverse To Laggers", ""])
    if inverse_leaders:
        for idx, row in enumerate(inverse_leaders[:10], start=1):
            lines.append(
                f"{idx}. `{row[entity_label]}` score `{row['relationship_score']:.2f}`, pairs `{row['pair_count']}`, best corr `{row['best_correlation']:+.4f}`, avg lag `{row['avg_lag_minutes']:.1f}m`"
            )
    else:
        lines.append("No inverse leaders passed the ranking filters.")

    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    base_dir = BREAKOUT_JSON_ROOT # [V20260510_1955]
    source_path = summary_net_path(base_dir, args.mode, args.product_type, args.date)
    if not source_path.exists():
        print(f"[ERROR] Source not found: {source_path}")
        return 1

    summary = load_summary(source_path)
    entity_label = "strategy" if args.grain == "strategy" else "strategy_product"
    aligned_times, series_map = (
        aggregate_strategy_series(summary) if args.grain == "strategy" else aggregate_product_series(summary)
    )
    if not series_map:
        print(f"[ERROR] No usable strategy series found in {source_path}")
        return 1

    candidate_names = select_analysis_universe(series_map, args.grain, args.candidate_limit)
    positive_relationships = build_relationship_rows(
        series_map,
        candidate_names,
        args.max_lag,
        args.min_points,
        relationship="positive",
    )
    inverse_relationships = build_relationship_rows(
        series_map,
        candidate_names,
        args.max_lag,
        args.min_points,
        relationship="inverse",
    )

    leaders = rank_entities_from_relationships(positive_relationships, "leader_strategy", entity_label, args.top_n)
    laggers = rank_entities_from_relationships(positive_relationships, "lagging_strategy", entity_label, args.top_n)
    inverse_leaders = rank_entities_from_relationships(inverse_relationships, "leader_strategy", entity_label, args.top_n)

    lead_lag_pairs = positive_relationships[: args.top_n]
    inverse_pairs = inverse_relationships[: args.top_n]

    output_payload = {
        "generated_at": datetime.now().isoformat(),
        "date": args.date,
        "mode": args.mode,
        "product_type": args.product_type,
        "grain": args.grain,
        "source": str(source_path),
        "snapshot_minutes": SNAPSHOT_MINUTES,
        "max_lag_steps": args.max_lag,
        "max_lag_minutes": args.max_lag * SNAPSHOT_MINUTES,
        "min_points": args.min_points,
        "candidate_universe_size": len(candidate_names),
        "series_count": len(series_map),
        "snapshot_count": len(aligned_times),
        "methodology": {
            "leading_definition": "earlier member of a positive-lag relationship",
            "lagging_definition": "later member of a similar relationship at a positive lag",
            "positive_lead_lag_metric": "maximum positive Pearson correlation of 15-minute net-change series with strictly positive lag",
            "inverse_lead_lag_metric": "minimum negative Pearson correlation of 15-minute net-change series with strictly positive lag",
            "entity_ranking": "sum of abs(correlation) * sample_points across qualifying directed relationships",
            "candidate_universe": "all strategy series" if args.grain == "strategy" else "highest-activity product-level entities by total absolute 15-minute net change",
        },
        "leading_entities": leaders,
        "lagging_entities": laggers,
        "leading_to_lagging_correlated": lead_lag_pairs,
        "inverse_lead_lag_relationships": inverse_pairs,
        "inverse_leading_entities": inverse_leaders,
    }
    if args.grain == "strategy":
        output_payload["leading_strategies"] = leaders
        output_payload["lagging_strategies"] = laggers
        output_payload["inverse_correlated_strategies"] = inverse_pairs
        output_payload["leading_to_lagging_inverse"] = inverse_leaders

    json_path = output_json_path(base_dir, args.mode, args.product_type, args.date, args.grain)
    md_path = output_md_path(base_dir, args.mode, args.product_type, args.date, args.grain)
    json_path.write_text(json.dumps(output_payload, indent=2), encoding="utf-8")
    md_path.write_text(
        build_report(
            args.date,
            args.mode,
            args.product_type,
            args.grain,
            source_path,
            len(aligned_times),
            len(candidate_names),
            leaders,
            laggers,
            lead_lag_pairs,
            inverse_pairs,
            inverse_leaders,
            args.max_lag,
        ),
        encoding="utf-8",
    )

    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")
    print(f"Leading entities: {len(leaders)}")
    print(f"Lagging entities: {len(laggers)}")
    print(f"Lead/lag pairs: {len(lead_lag_pairs)}")
    print(f"Inverse pairs: {len(inverse_pairs)}")
    print(f"Inverse leading entities: {len(inverse_leaders)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
