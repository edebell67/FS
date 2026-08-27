"""Deterministic constrained portfolio search.

Version history: 1.1.0 (2026-08-23) — bounded search and streaming best result.
1.0.0 (2026-08-23) — initial reference engine.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import math
import random
from dataclasses import dataclass, asdict
from typing import Iterable

ENGINE_VERSION = "1.0.0"
MAX_ELIGIBLE_CANDIDATES = 40
MAX_COMBINATIONS = 100_000


@dataclass(frozen=True)
class Candidate:
    strategy_id: str
    cluster: str
    market: str
    volatility: float
    quality: str = "VALID"
    closed_trades: int = 30


def _stable_hash(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _weights(selected: tuple[Candidate, ...], mode: str) -> dict[str, float]:
    if mode == "equal":
        raw = [1.0] * len(selected)
    elif mode == "risk_balanced":
        raw = [1.0 / max(item.volatility, 1e-9) for item in selected]
    else:
        raise ValueError(f"unsupported baseline: {mode}")
    total = sum(raw)
    result = {item.strategy_id: value / total for item, value in zip(selected, raw)}
    last = selected[-1].strategy_id
    result[last] += 1.0 - sum(result.values())
    return result


def _constraint_failures(selected: tuple[Candidate, ...], weights: dict[str, float], c: dict) -> list[str]:
    failures: list[str] = []
    if not c["minimum_strategies"] <= len(selected) <= c["maximum_strategies"]:
        failures.append("STRATEGY_COUNT")
    if any(weight > c["maximum_strategy_weight"] + 1e-12 for weight in weights.values()):
        failures.append("STRATEGY_WEIGHT")
    for field, cap, code in (("cluster", c["maximum_cluster_weight"], "CLUSTER_WEIGHT"), ("market", c["maximum_market_weight"], "MARKET_WEIGHT")):
        totals: dict[str, float] = {}
        for item in selected:
            totals[getattr(item, field)] = totals.get(getattr(item, field), 0) + weights[item.strategy_id]
        if any(value > cap + 1e-12 for value in totals.values()):
            failures.append(code)
    return sorted(set(failures))


def optimise(candidates: Iterable[Candidate], constraints: dict, *, seed: int, input_version: str) -> dict:
    """Select the lowest concentration/risk feasible set; returns a replayable manifest."""
    items = sorted(candidates, key=lambda x: x.strategy_id)
    eligible, exclusions = [], []
    for item in items:
        reasons = []
        if item.quality not in constraints["eligible_quality_states"]:
            reasons.append("QUALITY")
        if item.closed_trades < constraints["minimum_history_closed_trades"]:
            reasons.append("HISTORY")
        (exclusions if reasons else eligible).append({"strategy_id": item.strategy_id, "reasons": reasons} if reasons else item)

    minimum = constraints["minimum_strategies"]
    maximum = min(constraints["maximum_strategies"], len(eligible))
    if not 1 <= minimum <= maximum:
        return {"feasible": False, "reason_code": "INVALID_STRATEGY_COUNT", "eligible_count": len(eligible), "exclusions": exclusions}
    if len(eligible) > MAX_ELIGIBLE_CANDIDATES:
        return {"feasible": False, "reason_code": "CANDIDATE_BUDGET_EXCEEDED", "eligible_count": len(eligible), "maximum": MAX_ELIGIBLE_CANDIDATES, "exclusions": exclusions}
    combination_count = sum(math.comb(len(eligible), size) for size in range(minimum, maximum + 1))
    if combination_count > MAX_COMBINATIONS:
        return {"feasible": False, "reason_code": "SEARCH_BUDGET_EXCEEDED", "combination_count": combination_count, "maximum": MAX_COMBINATIONS, "exclusions": exclusions}

    rng = random.Random(seed)
    tie_breakers = {item.strategy_id: rng.random() for item in eligible}
    best = None
    for size in range(minimum, maximum + 1):
        for selected in itertools.combinations(eligible, size):
            for mode in ("equal", "risk_balanced"):
                weights = _weights(selected, mode)
                failures = _constraint_failures(selected, weights, constraints)
                if not failures:
                    concentration = sum(weight * weight for weight in weights.values())
                    risk_proxy = sum(weights[x.strategy_id] * x.volatility for x in selected)
                    score = risk_proxy + concentration + sum(tie_breakers[x.strategy_id] for x in selected) * 1e-9
                    candidate = (score, selected, weights, mode)
                    if best is None or score < best[0]:
                        best = candidate
    if best is None:
        return {"feasible": False, "reason_code": "NO_FEASIBLE_PORTFOLIO", "eligible_count": len(eligible), "exclusions": exclusions}

    _, selected, weights, mode = best
    inputs = [asdict(item) for item in items]
    return {
        "feasible": True,
        "engine_version": ENGINE_VERSION,
        "seed": seed,
        "input_version": input_version,
        "input_hash": _stable_hash(inputs),
        "constraint_hash": _stable_hash(constraints),
        "baseline": mode,
        "objective": "minimise risk proxy plus concentration; returns are not ranked",
        "allocations": weights,
        "exclusions": exclusions,
        "sensitivity": {"rerun_required_for": ["constraints", "input_version", "seed", "candidate_snapshot"]},
    }
