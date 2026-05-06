import csv
import json
import time
import uuid
import requests
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Trade:
    trade_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    signal: str = None
    entry_price: float = 0.0
    execution_mid_price: float = 0.0
    size: int = 0
    total_cost: float = 0.0
    open_pnl: float = 0.0
    realised_pnl: float = 0.0
    last_bank_level: float = 0.0
    adverse_reduce_steps_applied: int = 0
    favourable_add_steps_applied: int = 0
    execution_count: int = 1

    # Used for direction of movement, NOT entry comparison
    last_bid: float = None
    last_ask: float = None


@dataclass
class Variant:
    product: str
    name: str
    bank_threshold: float
    trades: list[Trade] = field(default_factory=list)
    banked_profit: float = 0.0
    realised_pnl: float = 0.0
    trade_count: int = 0


def load_config(path="config.json"):
    with open(path, "r") as f:
        return json.load(f)


def pip_size(product, cfg):
    return cfg.get("pip_sizes", {}).get(product, cfg["pip_size_default"])


def commission_value(product, size, cfg):
    return cfg["commission_pips"] * pip_size(product, cfg) * size


def stop_loss_amount(cfg):
    return float(cfg.get("stop_loss_amount", 50))


def adverse_reduce_pips(cfg):
    return float(cfg.get("adverse_reduce_pips", 3))


def adverse_reduce_size(cfg):
    return int(cfg.get("adverse_reduce_size", 10000))


def fetch_prices(cfg):
    response = requests.get(cfg["api_url"], timeout=10)
    response.raise_for_status()

    wanted = {p.lower() for p in cfg["products"]}
    prices = {}

    for row in response.json().get("data", []):
        code = str(row.get("code", "")).lower()
        if code in wanted and not row.get("stale", True):
            prices[code] = {
                "bid": float(row["bid"]),
                "ask": float(row["ask"]),
                "timestamp": row["timestamp"],
                "id": row.get("id"),
            }

    return prices


def ensure_header(path, columns):
    if not path.exists():
        with open(path, "w", newline="") as f:
            csv.writer(f).writerow(columns)


def get_run_timestamp(cfg):
    return cfg.setdefault("_run_timestamp", datetime.now().strftime("%Y%m%d_%H%M%S"))


def log_price(product, quote, cfg):
    out = Path(cfg["output_dir"])
    out.mkdir(exist_ok=True)

    path = out / f"{product}_price_replay_log.csv"
    ensure_header(path, ["captured_at", "source_timestamp", "product", "bid", "ask", "mid"])

    bid, ask = quote["bid"], quote["ask"]
    mid = (bid + ask) / 2

    with open(path, "a", newline="") as f:
        csv.writer(f).writerow([
            datetime.now().isoformat(), quote["timestamp"], product, bid, ask, mid
        ])


def exit_price(t, bid, ask):
    return bid if t.signal == "BUY" else ask


def entry_price_for_signal(signal, bid, ask):
    return ask if signal == "BUY" else bid


def current_mid_price(bid, ask):
    return (bid + ask) / 2


def pip_step_count(pips, step_size):
    return int((pips + 1e-9) // step_size)


def gross_pnl(t, bid, ask, size=None):
    if size is None:
        size = t.size

    if t.signal == "BUY":
        return (bid - t.entry_price) * size

    if t.signal == "SELL":
        return (t.entry_price - ask) * size

    return 0.0


def open_pnl(t, bid, ask):
    return gross_pnl(t, bid, ask, t.size) - t.total_cost


def open_pips(t, bid, ask, product, cfg):
    if not t.signal or t.size <= 0:
        return 0.0

    ps = pip_size(product, cfg)
    mid_delta = (current_mid_price(bid, ask) - t.execution_mid_price) / ps
    if t.signal == "BUY":
        return mid_delta
    return -mid_delta


def active_pnl(t):
    return t.realised_pnl + t.open_pnl


def variant_open_pnl(v):
    return sum(t.open_pnl for t in v.trades)


def total_profit(v):
    return v.banked_profit + v.realised_pnl + variant_open_pnl(v)


def create_trade(v, signal, bid, ask, cfg):
    size = cfg["start_size"]
    t = Trade(
        signal=signal,
        entry_price=entry_price_for_signal(signal, bid, ask),
        execution_mid_price=current_mid_price(bid, ask),
        size=size,
        total_cost=commission_value(v.product, size, cfg),
        last_bid=bid,
        last_ask=ask,
    )
    v.trades.append(t)
    v.trade_count += 1
    return t


def maybe_open_pair(v, bid, ask, cfg):
    if v.trades:
        return []

    buy = create_trade(v, "BUY", bid, ask, cfg)
    sell = create_trade(v, "SELL", bid, ask, cfg)

    return [
        (buy, "OPEN_BUY", "pair entry opened immediately"),
        (sell, "OPEN_SELL", "pair entry opened immediately"),
    ]


def add_size(v, t, bid, ask, cfg):
    qty = min(cfg["size_step"], cfg["max_size"] - t.size)
    if qty <= 0:
        return 0

    add_px = entry_price_for_signal(t.signal, bid, ask)
    add_mid = current_mid_price(bid, ask)
    new_size = t.size + qty
    t.entry_price = ((t.entry_price * t.size) + (add_px * qty)) / new_size
    t.execution_mid_price = ((t.execution_mid_price * t.size) + (add_mid * qty)) / new_size
    t.size = new_size
    t.total_cost += commission_value(v.product, qty, cfg)
    t.execution_count += 1
    return qty


def reduce_size(v, t, bid, ask, cfg, mode):
    reduce_chunk = adverse_reduce_size(cfg) if mode == "REDUCE" else cfg["size_step"]
    qty = min(reduce_chunk, t.size - cfg["min_size"])
    if qty <= 0:
        return 0.0

    realised = gross_pnl(t, bid, ask, qty) - commission_value(v.product, qty, cfg)

    old_size = t.size
    t.size -= qty

    if old_size > 0 and t.size > 0:
        t.total_cost = t.total_cost * (t.size / old_size)
    else:
        t.total_cost = 0.0

    if mode == "BANK":
        v.banked_profit += realised
        t.last_bank_level += v.bank_threshold
    else:
        t.realised_pnl += realised
        v.realised_pnl += realised

    t.execution_count += 1
    return realised


def close_trade(v, t, bid, ask, cfg):
    t.execution_count += 1
    realised = gross_pnl(t, bid, ask, t.size) - t.total_cost - commission_value(v.product, t.size, cfg)
    t.realised_pnl += realised
    v.realised_pnl += realised
    v.trades = [x for x in v.trades if x.trade_id != t.trade_id]
    return realised


def tick_direction(t, bid, ask):
    """
    Direction is based on current tick vs previous tick.

    BUY:
      bid up   = favourable
      bid down = against

    SELL:
      ask down = favourable
      ask up   = against

    Flat tick = neutral.
    """
    if t.last_bid is None or t.last_ask is None:
        return "NEUTRAL"

    if t.signal == "BUY":
        if bid > t.last_bid:
            return "FAVOURABLE"
        if bid < t.last_bid:
            return "AGAINST"
        return "NEUTRAL"

    if t.signal == "SELL":
        if ask < t.last_ask:
            return "FAVOURABLE"
        if ask > t.last_ask:
            return "AGAINST"
        return "NEUTRAL"

    return "NEUTRAL"


def update_last_prices(t, bid, ask):
    t.last_bid = bid
    t.last_ask = ask


def manage_trade(v, t, bid, ask, cfg):
    t.open_pnl = open_pnl(t, bid, ask)
    direction = tick_direction(t, bid, ask)
    favorable_pips = max(open_pips(t, bid, ask, v.product, cfg), 0.0)
    add_steps_due = pip_step_count(favorable_pips, adverse_reduce_pips(cfg))
    adverse_pips = max(-open_pips(t, bid, ask, v.product, cfg), 0.0)
    reduce_steps_due = pip_step_count(adverse_pips, adverse_reduce_pips(cfg))

    # 1. BANK FIRST IF PROFITABLE
    if t.open_pnl >= t.last_bank_level + v.bank_threshold and t.size > cfg["min_size"]:
        realised = reduce_size(v, t, bid, ask, cfg, "BANK")
        t.open_pnl = open_pnl(t, bid, ask)
        update_last_prices(t, bid, ask)
        return ("BANK_PROFIT", f"banked reduced slice P&L={realised:.2f}")

    # 2. REDUCE AFTER EACH NEW 3-PIP ADVERSE BAND, BUT NEVER BELOW MIN SIZE.
    # Do NOT full-close a large position just because stop is breached.
    # The final 1k is reserved for the explicit stop-loss close.
    if reduce_steps_due > t.adverse_reduce_steps_applied and t.size > cfg["min_size"]:
        realised = reduce_size(v, t, bid, ask, cfg, "REDUCE")
        if realised != 0.0:
            t.adverse_reduce_steps_applied += 1
        t.open_pnl = open_pnl(t, bid, ask)
        update_last_prices(t, bid, ask)
        return (
            "REDUCE_SIZE",
            f"adverse move reached {adverse_pips:.1f} pips; reduced size by {adverse_reduce_size(cfg)}",
        )

    # 3. STOP LOSS ONLY WHEN ALREADY AT MIN SIZE
    if t.size == cfg["min_size"] and active_pnl(t) <= -stop_loss_amount(cfg):
        realised = close_trade(v, t, bid, ask, cfg)
        return ("STOP_LOSS", f"min-size stop loss hit; closed remaining P&L={realised:.2f}")

    # 4. ADD AFTER EACH NEW 3-PIP FAVOURABLE BAND WHILE PROFITABLE.
    if add_steps_due > t.favourable_add_steps_applied and t.open_pnl > 0 and t.size < cfg["max_size"]:
        qty = add_size(v, t, bid, ask, cfg)
        if qty > 0:
            t.favourable_add_steps_applied += 1
        t.open_pnl = open_pnl(t, bid, ask)
        update_last_prices(t, bid, ask)
        return ("ADD_SIZE", f"favourable move reached {favorable_pips:.1f} pips; added size={qty}")

    update_last_prices(t, bid, ask)

    if t.size == cfg["min_size"]:
        return ("HOLD_MIN_SIZE", "holding min size until stop or recovery")

    return ("HOLD_SIZE", "neutral/no qualifying action")


def log_decision(v, t, action, reason, bid, ask, cfg):
    out = Path(cfg["output_dir"])
    out.mkdir(exist_ok=True)

    run_timestamp = get_run_timestamp(cfg)
    path = out / f"{v.product}_decision_log_{run_timestamp}.csv"
    columns = [
        "timestamp", "product", "variant", "bank_threshold", "trade_id",
        "action", "reason", "signal", "size", "bid", "ask", "entry_price",
        "exit_price", "open_pips", "open_pnl", "trade_realised_pnl",
        "active_pnl", "banked_profit", "variant_realised_pnl",
        "variant_open_pnl", "total_profit", "trade_count", "total_cost",
        "open_trade_count", "execution_count", "last_bid", "last_ask"
    ]
    ensure_header(path, columns)

    with open(path, "a", newline="") as f:
        csv.writer(f).writerow([
            datetime.now().isoformat(), v.product, v.name, v.bank_threshold,
            t.trade_id, action, reason, t.signal, t.size, bid, ask,
            t.entry_price, exit_price(t, bid, ask), open_pips(t, bid, ask, v.product, cfg),
            t.open_pnl, t.realised_pnl, active_pnl(t), v.banked_profit,
            v.realised_pnl, variant_open_pnl(v), total_profit(v),
            v.trade_count, t.total_cost, len(v.trades), t.execution_count, t.last_bid, t.last_ask
        ])


def existing_signals(v):
    return {t.signal for t in v.trades}


def maintain_buy_sell(v, bid, ask, cfg):
    """
    Invariant:
      Each variant maintains one BUY and one SELL.

    If either side is missing, recreate it immediately at start_size.
    This is not a strategy rule; it is the required operating structure.
    """
    opened = []
    signals = existing_signals(v)

    if "BUY" not in signals:
        buy = create_trade(v, "BUY", bid, ask, cfg)
        buy.open_pnl = open_pnl(buy, bid, ask)
        opened.append((buy, "OPEN_BUY", "BUY side recreated to maintain BUY+SELL pair"))

    if "SELL" not in signals:
        sell = create_trade(v, "SELL", bid, ask, cfg)
        sell.open_pnl = open_pnl(sell, bid, ask)
        opened.append((sell, "OPEN_SELL", "SELL side recreated to maintain BUY+SELL pair"))

    return opened


def build_variants(cfg):
    return [
        Variant(product=p.lower(), name=f"{p.lower()}_bank_{b}", bank_threshold=b)
        for p in cfg["products"]
        for b in cfg["bank_variants"]
    ]


def print_status(variants, prices, cfg):
    print("\n--- STATUS ---")

    for v in variants:
        q = prices.get(v.product, {})
        bid = q.get("bid", 0.0)
        ask = q.get("ask", 0.0)

        if not v.trades:
            print(
                f"{v.name:<18} | bid={bid:<10.5f} | ask={ask:<10.5f} | "
                f"open_trades=0 | banked={v.banked_profit:>8.2f} | "
                f"realised={v.realised_pnl:>8.2f} | open={0.0:>8.2f} | "
                f"total={total_profit(v):>8.2f} | pair_entries={v.trade_count}"
            )
            continue

        for idx, t in enumerate(v.trades, start=1):
            print(
                f"{v.name:<18} | T{idx}:{t.signal:<4} | "
                f"bid={bid:<10.5f} | ask={ask:<10.5f} | "
                f"entry={t.entry_price:<10.5f} | exit={exit_price(t,bid,ask):<10.5f} | "
                f"pips={open_pips(t,bid,ask,v.product,cfg):>7.1f} | "
                f"active={active_pnl(t):>8.2f} | open={t.open_pnl:>8.2f} | "
                f"size={t.size:>6} | banked={v.banked_profit:>8.2f} | "
                f"realised={v.realised_pnl:>8.2f} | total={total_profit(v):>8.2f} | "
                f"execs={t.execution_count:>3} | pair_entries={v.trade_count}"
            )


def run():
    cfg = load_config()
    variants = build_variants(cfg)

    while True:
        prices = fetch_prices(cfg)

        for product, q in prices.items():
            bid, ask = q["bid"], q["ask"]
            log_price(product, q, cfg)

            for v in [x for x in variants if x.product == product]:
                # First valid quote opens both sides.
                entries = maybe_open_pair(v, bid, ask, cfg)

                if entries:
                    for t, action, reason in entries:
                        t.open_pnl = open_pnl(t, bid, ask)
                        log_decision(v, t, action, reason, bid, ask, cfg)
                else:
                    # Manage each active leg independently.
                    for t in list(v.trades):
                        decision = manage_trade(v, t, bid, ask, cfg)
                        if decision:
                            log_decision(v, t, decision[0], decision[1], bid, ask, cfg)

                    # Maintain invariant: one BUY and one SELL must exist.
                    recreated = maintain_buy_sell(v, bid, ask, cfg)
                    for t, action, reason in recreated:
                        log_decision(v, t, action, reason, bid, ask, cfg)

        print_status(variants, prices, cfg)
        time.sleep(cfg["poll_seconds"])


if __name__ == "__main__":
    run()
