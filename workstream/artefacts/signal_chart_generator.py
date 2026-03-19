from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.dates as mdates
import matplotlib.pyplot as plt


@dataclass
class TradeContext:
    trade_id: str
    strategy: str
    product: str
    direction: str
    entry_time: datetime
    entry_price: float
    current_price: float
    tp_price: float
    sl_price: float
    status: str
    trade_path: Path | None = None


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def parse_timestamp(value: str) -> datetime:
    normalized = value.replace("Z", "+00:00")
    return datetime.fromisoformat(normalized)


def to_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def derive_tp_sl_prices(entry_price: float, direction: str, tp_pips: Any, sl_pips: Any, pip_buffer: Any) -> tuple[float, float]:
    tp_delta = to_float(tp_pips) * to_float(pip_buffer)
    sl_delta = to_float(sl_pips) * to_float(pip_buffer)
    side = str(direction).upper()
    if side in {"SELL", "SHORT"}:
        return entry_price - tp_delta, entry_price + sl_delta
    return entry_price + tp_delta, entry_price - sl_delta


def trade_context_from_trade_file(trade_path: Path) -> TradeContext:
    trade = load_json(trade_path)
    entry_price = to_float(trade.get("entry_price"))
    current_price = to_float(trade.get("current_price", trade.get("exit_price", entry_price)), entry_price)
    tp_price, sl_price = derive_tp_sl_prices(
        entry_price=entry_price,
        direction=str(trade.get("direction", "LONG")),
        tp_pips=trade.get("tp_pips"),
        sl_pips=trade.get("sl_pips"),
        pip_buffer=trade.get("pip_buffer", 0.0001),
    )
    return TradeContext(
        trade_id=str(trade.get("trade_id", "unknown")),
        strategy=str(trade.get("source_strategy") or trade.get("script_name") or "unknown"),
        product=str(trade.get("product", "unknown")),
        direction=str(trade.get("direction", "LONG")),
        entry_time=parse_timestamp(str(trade["entry_time"])),
        entry_price=entry_price,
        current_price=current_price,
        tp_price=tp_price,
        sl_price=sl_price,
        status=str(trade.get("status") or trade.get("trade_status") or "UNKNOWN"),
        trade_path=trade_path,
    )


def trade_context_from_feed(feed_path: Path, signal_id: str | None) -> TradeContext:
    feed = load_json(feed_path)
    open_trades = feed.get("open_trades") or []
    signals = feed.get("signals") or []
    if not open_trades:
        raise ValueError("Feed does not contain open_trades entries")

    selected_trade = open_trades[0]
    if signal_id:
        matching_signal = next((item for item in signals if str(item.get("signal_id")) == signal_id), None)
        if matching_signal is None:
            raise ValueError(f"Signal id not found in feed: {signal_id}")
        selected_trade = next(
            (
                item
                for item in open_trades
                if str(item.get("strategy_id")) == str(matching_signal.get("strategy_id"))
                and str(item.get("pair")) == str(matching_signal.get("pair"))
            ),
            selected_trade,
        )

    entry_price = to_float(selected_trade.get("entry"))
    current_price = to_float(selected_trade.get("current_price", selected_trade.get("entry")), entry_price)
    tp_price = to_float(selected_trade.get("tp"), entry_price)
    sl_price = to_float(selected_trade.get("sl"), entry_price)
    return TradeContext(
        trade_id=str(selected_trade.get("trade_id", "unknown")),
        strategy=str(selected_trade.get("strategy_id", "unknown")),
        product=str(selected_trade.get("pair", "unknown")),
        direction=str(selected_trade.get("side", "LONG")),
        entry_time=datetime.utcnow(),
        entry_price=entry_price,
        current_price=current_price,
        tp_price=tp_price,
        sl_price=sl_price,
        status=str(selected_trade.get("status", "UNKNOWN")),
        trade_path=None,
    )


def list_trade_files(day_dir: Path) -> list[Path]:
    return [path for path in day_dir.glob("*.json") if not path.name.startswith("_")]


def build_point(timestamp: datetime, price: float, label: str) -> dict[str, Any]:
    return {"time": timestamp, "price": price, "label": label}


def find_price_history(day_dir: Path, context: TradeContext) -> list[dict[str, Any]]:
    points: list[dict[str, Any]] = []
    live_trades_path = day_dir / "_live_trades.json"
    if live_trades_path.exists():
        live_trades = load_json(live_trades_path).get("trades", [])
        for trade in live_trades:
            strategy = str(trade.get("source_strategy") or trade.get("script_name") or "")
            product = str(trade.get("product") or "")
            if strategy != context.strategy or product != context.product:
                continue
            append_trade_price_points(points, trade)
    else:
        for path in list_trade_files(day_dir):
            try:
                trade = load_json(path)
            except Exception:
                continue
            strategy = str(trade.get("source_strategy") or trade.get("script_name") or "")
            product = str(trade.get("product") or "")
            if strategy != context.strategy or product != context.product:
                continue
            append_trade_price_points(points, trade)

    if context.trade_path is not None and context.trade_path.exists():
        trade = load_json(context.trade_path)
        points.append(build_point(context.entry_time, context.entry_price, "selected_entry"))
        current_time_value = trade.get("exit_time") or trade.get("sent_at") or trade.get("tb_leader_set_at") or trade.get("entry_time")
        if current_time_value:
            points.append(build_point(parse_timestamp(str(current_time_value)), context.current_price, "selected_current"))

    deduped: dict[tuple[str, float], dict[str, Any]] = {}
    for point in points:
        key = (point["time"].isoformat(), round(point["price"], 8))
        deduped[key] = point
    ordered = sorted(deduped.values(), key=lambda item: item["time"])
    if len(ordered) >= 2:
        return ordered

    synthetic_end = context.entry_time.replace(minute=(context.entry_time.minute + 30) % 60)
    if synthetic_end <= context.entry_time:
        synthetic_end = context.entry_time
    return [
        build_point(context.entry_time, context.entry_price, "entry"),
        build_point(synthetic_end, context.current_price, "current"),
    ]


def append_trade_price_points(points: list[dict[str, Any]], trade: dict[str, Any]) -> None:
    entry_time = trade.get("entry_time")
    if entry_time:
        points.append(build_point(parse_timestamp(str(entry_time)), to_float(trade.get("entry_price")), "entry"))

    exit_time = trade.get("exit_time")
    exit_price = trade.get("exit_price")
    if exit_time and exit_price is not None:
        points.append(build_point(parse_timestamp(str(exit_time)), to_float(exit_price), "exit"))
    elif trade.get("current_price") is not None:
        current_time_value = trade.get("sent_at") or trade.get("tb_leader_set_at") or entry_time
        if current_time_value:
            points.append(build_point(parse_timestamp(str(current_time_value)), to_float(trade.get("current_price")), "current"))


def render_signal_chart(context: TradeContext, price_points: list[dict[str, Any]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    times = [point["time"] for point in price_points]
    prices = [point["price"] for point in price_points]
    direction = str(context.direction).upper()
    line_color = "#0f766e" if direction in {"BUY", "LONG"} else "#b91c1c"
    bg_color = "#f8fafc"

    fig, ax = plt.subplots(figsize=(12, 7), constrained_layout=True)
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor("white")

    ax.plot(times, prices, color=line_color, linewidth=2.5, marker="o", markersize=4)
    ax.axhline(context.entry_price, color="#1d4ed8", linestyle="--", linewidth=1.2, label=f"Entry {context.entry_price:.5f}")
    ax.axhline(context.tp_price, color="#15803d", linestyle=":", linewidth=1.2, label=f"TP {context.tp_price:.5f}")
    ax.axhline(context.sl_price, color="#dc2626", linestyle=":", linewidth=1.2, label=f"SL {context.sl_price:.5f}")
    ax.scatter([times[-1]], [prices[-1]], color="#111827", s=40, zorder=5)

    for point in price_points[-3:]:
        ax.annotate(
            point["label"],
            (point["time"], point["price"]),
            textcoords="offset points",
            xytext=(0, 8),
            ha="center",
            fontsize=8,
            color="#334155",
        )

    ax.set_title(f"{context.strategy} | {context.product} | {direction}", fontsize=16, fontweight="bold", color="#0f172a")
    ax.set_xlabel("Time")
    ax.set_ylabel("Price")
    ax.grid(True, alpha=0.2)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    fig.autofmt_xdate()

    summary = (
        f"Trade {context.trade_id}  Status {context.status}  "
        f"Entry {context.entry_price:.5f}  Current {context.current_price:.5f}"
    )
    ax.text(0.01, 0.01, summary, transform=ax.transAxes, fontsize=10, color="#334155")
    ax.legend(loc="upper left")

    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a signal chart image from workspace trade data.")
    parser.add_argument("--day-dir", required=True, help="Live day directory containing trade JSON files.")
    parser.add_argument("--trade-file", help="Specific trade JSON file to render.")
    parser.add_argument("--feed", help="Mini-app feed JSON path.")
    parser.add_argument("--signal-id", help="Signal identifier to resolve when using --feed.")
    parser.add_argument("--out", required=True, help="Output PNG path.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    day_dir = Path(args.day_dir)
    output_path = Path(args.out)

    if args.trade_file:
        context = trade_context_from_trade_file(Path(args.trade_file))
    elif args.feed:
        context = trade_context_from_feed(Path(args.feed), args.signal_id)
    else:
        raise SystemExit("Either --trade-file or --feed must be provided.")

    price_points = find_price_history(day_dir, context)
    render_signal_chart(context, price_points, output_path)

    print(output_path)
    print(
        json.dumps(
            {
                "strategy": context.strategy,
                "product": context.product,
                "direction": context.direction,
                "price_points": len(price_points),
                "image_bytes": output_path.stat().st_size,
            }
        )
    )


if __name__ == "__main__":
    main()
