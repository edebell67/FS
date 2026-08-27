# workstreams/WF-201/analytics.py — Deterministic closed-trade headline analytics.
#
# VERSION HISTORY
# v1.0.0 · 2026-08-23 · Initial version: calculates return, outcome, holding, excursion, equity, drawdown, and quality metadata without double-counting costs.

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from statistics import median
from typing import Any

ZERO = Decimal("0")
Q = Decimal("0.00000001")


def ratio(numerator: Decimal, denominator: Decimal) -> Decimal | None:
    return (numerator / denominator).quantize(Q) if denominator else None


def calculate_headline(trades: list[dict[str, Any]], *, starting_equity: Decimal | None = None, methodology_version: str = "1.0.0") -> dict[str, Any]:
    closed = [trade for trade in trades if trade.get("record_role") == "closed"]
    closed.sort(key=lambda item: (item["exit_at"], item["guid"]))
    returns = [Decimal(str(item["net_return"])) for item in closed]
    wins = [value for value in returns if value > 0]
    losses = [value for value in returns if value < 0]
    breakevens = [value for value in returns if value == 0]
    total = sum(returns, ZERO)
    gross_profit = sum(wins, ZERO)
    gross_loss = abs(sum(losses, ZERO))
    equity = starting_equity or ZERO
    peak = equity
    maximum_drawdown = ZERO
    for value in returns:
        equity += value
        peak = max(peak, equity)
        maximum_drawdown = min(maximum_drawdown, equity - peak)
    holding = [Decimal(str((item["exit_at"] - item["created_at"]).total_seconds())) / Decimal(60) for item in closed]
    mfe = [Decimal(str(item["max_net_return"])) for item in closed if item.get("max_net_return") is not None]
    mae = [Decimal(str(item["min_net_return"])) for item in closed if item.get("min_net_return") is not None]
    count = len(closed)
    mean = ratio(total, Decimal(count)) if count else None
    average_win = ratio(gross_profit, Decimal(len(wins))) if wins else None
    average_loss = ratio(sum(losses, ZERO), Decimal(len(losses))) if losses else None
    result = {
        "methodology_version": methodology_version,
        "total_trades": count,
        "wins": len(wins), "losses": len(losses), "breakevens": len(breakevens),
        "total_net_return": total.quantize(Q),
        "mean_trade": mean,
        "median_trade": Decimal(str(median(returns))).quantize(Q) if returns else None,
        "gross_profit": gross_profit.quantize(Q), "gross_loss": gross_loss.quantize(Q),
        "win_rate": ratio(Decimal(len(wins)), Decimal(count)) if count else None,
        "profit_factor": ratio(gross_profit, gross_loss),
        "average_win": average_win, "average_loss": average_loss,
        "payoff_ratio": ratio(average_win, abs(average_loss)) if average_win is not None and average_loss is not None else None,
        "expectancy": mean,
        "max_drawdown_money": maximum_drawdown.quantize(Q),
        "max_drawdown_percent": ratio(maximum_drawdown, starting_equity) if starting_equity else None,
        "mean_holding_minutes": ratio(sum(holding, ZERO), Decimal(len(holding))) if holding else None,
        "median_holding_minutes": Decimal(str(median(holding))).quantize(Q) if holding else None,
        "mean_mfe": ratio(sum(mfe, ZERO), Decimal(len(mfe))) if mfe else None,
        "mean_mae": ratio(sum(mae, ZERO), Decimal(len(mae))) if mae else None,
        "sample_sufficiency": "SUFFICIENT" if count >= 30 else "INSUFFICIENT",
        "quality_state": "VALID" if count else "NO_DATA",
        "calculated_at": datetime.now(timezone.utc),
    }
    return result

