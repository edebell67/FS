import json
import os
import re
import shutil
import sys
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen

# ---------------------------------------------------
# Configuration
# ---------------------------------------------------
HTTP_SOURCE_URL = "http://127.0.0.1:8002/api/vw_000_fx_quotes"
POLL_INTERVAL = 0.5
BUCKET_MINUTES = 5
MAX_COLUMNS = 15  # Show last 75 minutes (15 buckets)
GBP_PREFIX = "GBP"
ANSI_GREEN = "\033[92m"
ANSI_RED = "\033[91m"
ANSI_BRIGHT = "\033[1m"
ANSI_DIM = "\033[2m"
ANSI_RESET = "\033[0m"
ANSI_PATTERN = re.compile(r"\x1b\[[0-9;]*m")
PRICE_LABEL_WIDTH = 11
MAX_TRADE_EVENT_LINES = 18
TRADE_SIGNAL_LOG_FILE = Path(__file__).resolve().parent / "price_frequency_gbp_analyzer_trade_signals.txt"
SNAPSHOT_INTERVAL_SECONDS = 5

# ---------------------------------------------------
# Load config for snapshot storage path
# ---------------------------------------------------
BREAKOUT_CONFIG_PATH = Path(__file__).resolve().parents[3] / "TradeApps" / "breakout" / "fs" / "config.json"
GENERATED_DATA_ROOT = None
try:
    with open(BREAKOUT_CONFIG_PATH, "r", encoding="utf-8") as f:
        _config = json.load(f)
        GENERATED_DATA_ROOT = Path(_config.get("path_settings", {}).get("generated_data_root", "X:\\eds"))
except (FileNotFoundError, json.JSONDecodeError):
    GENERATED_DATA_ROOT = Path("X:\\eds")

# ---------------------------------------------------
# Global state
# ---------------------------------------------------
# data[symbol][side][price][bucket_time] = count
# bucket_time is HH:MM string of the interval start
price_data = defaultdict(
    lambda: {
        "bid": defaultdict(lambda: defaultdict(int)),
        "ask": defaultdict(lambda: defaultdict(int)),
    }
)
first_prices = defaultdict(
    lambda: {
        "bid": {},
        "ask": {},
    }
)
trade_marker_history = defaultdict(
    lambda: {
        "bid": defaultdict(lambda: defaultdict(list)),
        "ask": defaultdict(lambda: defaultdict(list)),
    }
)
bucket_times = []
last_timestamp_str = None
last_pulse_phase = None
last_trade_state_by_symbol = {}
recent_trade_events = []
active_position_by_symbol = {}
last_snapshot_time = 0


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def defaultdict_to_dict(obj):
    """Recursively convert defaultdicts to regular dicts for JSON serialization."""
    if isinstance(obj, defaultdict):
        return {k: defaultdict_to_dict(v) for k, v in obj.items()}
    elif isinstance(obj, dict):
        return {k: defaultdict_to_dict(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [defaultdict_to_dict(item) for item in obj]
    return obj


last_raw_prices = {}


def capture_snapshot():
    """Capture raw bid/ask prices for all products to single JSONL file."""
    global last_snapshot_time
    if not last_raw_prices:
        return

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")

    snapshot_dir = GENERATED_DATA_ROOT / "TradeApps" / "breakout" / "fs" / "json" / "live" / "forex" / date_str
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    snapshot_file = snapshot_dir / "_price_capture.jsonl"

    snapshot_data = {"ts": now.isoformat()}
    snapshot_data.update(last_raw_prices)

    try:
        with open(snapshot_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(snapshot_data) + "\n")
    except OSError:
        pass

    last_snapshot_time = time.time()


def get_bucket_time(dt):
    """Align datetime to the start of the 5-minute bucket."""
    minute = (dt.minute // BUCKET_MINUTES) * BUCKET_MINUTES
    return dt.replace(minute=minute, second=0, microsecond=0).strftime("%H:%M")


def parse_quote_timestamp(timestamp_str):
    try:
        return datetime.fromisoformat(timestamp_str).replace(tzinfo=None)
    except ValueError:
        pass
    try:
        return datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        return datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")


def fetch_quotes():
    with urlopen(HTTP_SOURCE_URL, timeout=5) as response:
        payload = json.load(response)
    return payload.get("data", [])


def is_gbp_symbol(symbol):
    return str(symbol or "").upper() == "GBPAUD_C"


def compute_side_metrics(symbol, side, bucket_time):
    open_price = first_prices[symbol][side].get(bucket_time)
    above_pressure = 0
    at_open_count = 0
    below_pressure = 0

    for price, bucket_counts in price_data[symbol][side].items():
        count = bucket_counts.get(bucket_time, 0)
        if count <= 0 or open_price is None:
            continue
        signed_count = -count if price < open_price else count
        if price > open_price and signed_count > 0:
            above_pressure += signed_count
        elif price == open_price:
            at_open_count += abs(signed_count)
        elif price < open_price and signed_count < 0:
            below_pressure += abs(signed_count)

    net_pressure = above_pressure - below_pressure
    directional_total = above_pressure + below_pressure
    pressure_ratio = round(above_pressure / directional_total, 4) if directional_total > 0 else None
    return {
        "open": open_price,
        "above": above_pressure,
        "at_open": at_open_count,
        "below": below_pressure,
        "net": net_pressure,
        "directional_total": directional_total,
        "ratio": pressure_ratio,
    }


def classify_state(bid_metrics, ask_metrics, current_open, prior_open):
    bid_net = bid_metrics["net"]
    ask_net = ask_metrics["net"]
    open_move = None
    if current_open is not None and prior_open is not None:
        if current_open > prior_open:
            open_move = "higher"
        elif current_open < prior_open:
            open_move = "lower"
        else:
            open_move = "flat"

    state = "FLAT_NO_EDGE"
    key_transition = "Balanced or insufficient evidence."
    confirmation = "Need BID/ASK alignment with clearer pressure or next-open confirmation."

    if bid_net > 0 and ask_net > 0:
        if (
            bid_net >= 20
            and ask_net >= 20
            and (bid_metrics["below"] == 0 or bid_net >= 10)
            and (ask_metrics["below"] == 0 or ask_net >= 10)
        ):
            state = "LONG_ENTRY_CANDIDATE_HIGH"
            key_transition = "Strong upward pressure / active recovery / continuation."
            confirmation = "Need next open higher than current open for full confirmation."
        elif (
            bid_net >= 10
            and ask_net >= 10
            and (bid_metrics["below"] == 0 or bid_net >= 10)
            and (ask_metrics["below"] == 0 or ask_net >= 10)
        ):
            state = "LONG_ENTRY_CANDIDATE_MEDIUM"
            key_transition = "Positive pressure is validated on BID and ASK."
            confirmation = "Need next open higher than current open for stronger confirmation."
        elif (
            bid_net >= 6
            and ask_net >= 6
            and bid_metrics["above"] > bid_metrics["below"]
            and ask_metrics["above"] > ask_metrics["below"]
        ):
            state = "LONG_ENTRY_CANDIDATE_LOW"
            key_transition = "Moderate upside pressure is present, but not aggressive."
            confirmation = "Need next open higher and stronger above-open pressure for confidence."
        elif 1 <= bid_net <= 5 and 1 <= ask_net <= 5:
            state = "MILD_REPAIR"
            key_transition = "Mild repair / stabilisation. Not a confirmed reversal."
            confirmation = "Need BID and ASK to strengthen beyond +5 before treating this as an entry."
        elif (bid_metrics["below"] == 0 or bid_net >= 10) and (ask_metrics["below"] == 0 or ask_net >= 10):
            confidence = "MEDIUM" if bid_net >= 6 and ask_net >= 6 else "LOW"
            state = f"LONG_ENTRY_CANDIDATE_{confidence}"
            key_transition = "Short-term recovery pressure has flipped positive."
            confirmation = "Need next open higher than current open for full confirmation."
        else:
            state = "HOLD_LONG_WEAKENING"
            key_transition = "Positive pressure present but not clean enough for strong entry."
            confirmation = "Need stronger above-open pressure or zero below-open pressure."
    elif bid_net < 0 and ask_net < 0:
        if (
            bid_net <= -20
            and ask_net <= -20
            and (bid_metrics["above"] == 0 or bid_net <= -10)
            and (ask_metrics["above"] == 0 or ask_net <= -10)
        ):
            state = "SHORT_ENTRY_CANDIDATE_HIGH"
            key_transition = "Strong downside continuation / failed open / rejection."
            confirmation = "Need next open lower than current open for full confirmation."
        elif (
            bid_net <= -10
            and ask_net <= -10
            and (bid_metrics["above"] == 0 or bid_net <= -10)
            and (ask_metrics["above"] == 0 or ask_net <= -10)
        ):
            state = "SHORT_ENTRY_CANDIDATE_MEDIUM"
            key_transition = "Downside pressure is active and validated."
            confirmation = "Need next open lower than current open for stronger confirmation."
        elif (
            bid_net <= -6
            and ask_net <= -6
            and bid_metrics["below"] > bid_metrics["above"]
            and ask_metrics["below"] > ask_metrics["above"]
        ):
            state = "SHORT_ENTRY_CANDIDATE_LOW"
            key_transition = "Moderate downside pressure is active."
            confirmation = "Need next open lower and stronger below-open pressure for confidence."
        elif -5 <= bid_net <= -1 and -5 <= ask_net <= -1:
            state = "MILD_DOWNSIDE"
            key_transition = "Mild downward pressure / leakage below open."
            confirmation = "Need BID and ASK to weaken beyond -5 before treating this as an entry."
        elif (bid_metrics["above"] == 0 or bid_net <= -10) and (ask_metrics["above"] == 0 or ask_net <= -10):
            confidence = "MEDIUM" if bid_net <= -6 and ask_net <= -6 else "LOW"
            state = f"SHORT_ENTRY_CANDIDATE_{confidence}"
            key_transition = "Downside pressure is active below the open."
            confirmation = "Need next open lower than current open for full confirmation."
        else:
            state = "HOLD_SHORT_WEAKENING"
            key_transition = "Negative pressure present but not yet a strong downside continuation."
            confirmation = "Need stronger below-open pressure or zero above-open pressure."
    elif -3 <= bid_net <= 3 or -3 <= ask_net <= 3:
        state = "FLAT_NO_EDGE"
        key_transition = "Balanced / holding / no clean directional edge."
        confirmation = "Wait for BID and ASK to separate clearly from zero."

    if open_move == "higher" and bid_net < 0 and ask_net < 0:
        state = "EXIT_LONG_CANDIDATE_HIGH"
        key_transition = "Failed higher open. Price opened higher but activity built below the open."
        confirmation = "Confirmed if next open drops or downside pressure deepens."
    elif open_move == "lower" and bid_net > 0 and ask_net > 0:
        state = "EXIT_SHORT_CANDIDATE_HIGH"
        key_transition = "Lower-open bounce / repair attempt."
        confirmation = "Confirmed if next open rises or upside pressure strengthens."

    return state, key_transition, confirmation, open_move


def format_open_price(value):
    return f"{value:.4f}" if value is not None else "n/a"


def select_trigger_price(symbol, side, bucket_time, mode):
    open_price = first_prices[symbol][side].get(bucket_time)
    if open_price is None:
        return None

    candidate = None
    best_strength = -1
    for price, bucket_counts in price_data[symbol][side].items():
        count = bucket_counts.get(bucket_time, 0)
        if count <= 0:
            continue
        signed_count = -count if price < open_price else count
        if mode == "above" and price > open_price and signed_count > 0:
            strength = signed_count
        elif mode == "below" and price < open_price and signed_count < 0:
            strength = abs(signed_count)
        else:
            continue

        if strength > best_strength:
            best_strength = strength
            candidate = price

    return candidate if candidate is not None else open_price


def get_bucket_marker(symbol, bucket_time, previous_bucket=None):
    bid_metrics = compute_side_metrics(symbol, "bid", bucket_time)
    ask_metrics = compute_side_metrics(symbol, "ask", bucket_time)
    prior_open = first_prices[symbol]["bid"].get(previous_bucket) if previous_bucket else None
    current_open = bid_metrics["open"]
    state, _, _, _ = classify_state(bid_metrics, ask_metrics, current_open, prior_open)

    if state.startswith("LONG_ENTRY_CANDIDATE"):
        return {
            "state": state,
            "side": "ask",
            "style": "open",
            "price": select_trigger_price(symbol, "ask", bucket_time, "above"),
        }
    if state.startswith("EXIT_LONG"):
        return {
            "state": state,
            "side": "ask",
            "style": "close",
            "price": select_trigger_price(symbol, "ask", bucket_time, "below"),
        }
    if state.startswith("SHORT_ENTRY_CANDIDATE"):
        return {
            "state": state,
            "side": "bid",
            "style": "open",
            "price": select_trigger_price(symbol, "bid", bucket_time, "below"),
        }
    if state.startswith("EXIT_SHORT"):
        return {
            "state": state,
            "side": "bid",
            "style": "close",
            "price": select_trigger_price(symbol, "bid", bucket_time, "above"),
        }
    return None


def marker_position_direction(marker_info):
    if not marker_info:
        return None
    state = str(marker_info.get("state", ""))
    if "LONG" in state:
        return "long"
    if "SHORT" in state:
        return "short"
    side = marker_info.get("side")
    if side == "ask":
        return "long"
    if side == "bid":
        return "short"
    return None


def infer_pip_multiplier(symbol):
    symbol_upper = str(symbol or "").upper()
    return 100 if "JPY" in symbol_upper else 10000


def compute_net_pips(symbol, direction, entry_price, exit_price):
    multiplier = infer_pip_multiplier(symbol)
    if direction == "long":
        return round((exit_price - entry_price) * multiplier, 1)
    if direction == "short":
        return round((entry_price - exit_price) * multiplier, 1)
    return None


def should_record_trade_event(symbol, marker_info):
    if not marker_info or marker_info.get("price") is None:
        return False
    direction = marker_position_direction(marker_info)
    style = marker_info.get("style")
    active_position = active_position_by_symbol.get(symbol)
    active_direction = active_position.get("direction") if active_position else None

    if style == "open":
        if active_direction is not None:
            return False
        active_position_by_symbol[symbol] = {
            "direction": direction,
            "entry_price": marker_info.get("price"),
            "entry_timestamp": marker_info.get("timestamp"),
            "entry_bucket": marker_info.get("bucket"),
            "entry_state": marker_info.get("state"),
            "entry_side": marker_info.get("side"),
        }
        return True

    if style == "close":
        if active_direction is None:
            return False
        if direction != active_direction:
            return False
        marker_info["entry_price"] = active_position.get("entry_price")
        marker_info["entry_timestamp"] = active_position.get("entry_timestamp")
        marker_info["net_pips"] = compute_net_pips(
            symbol,
            active_direction,
            active_position.get("entry_price"),
            marker_info.get("price"),
        )
        active_position_by_symbol.pop(symbol, None)
        return True

    return False


def append_trade_signal_log(event):
    line = (
        f"{event['timestamp']} | symbol={event['symbol']} | side={event['side']} | "
        f"event={event['event']} | bucket={event['bucket']} | price={event['price']:.4f} | "
        f"count={event['signed_count']} | marker={event['marker']} | state={event['state']}"
    )
    if event.get("event") == "CLOSE" and event.get("net_pips") is not None:
        line += f" | entry_price={event['entry_price']:.4f} | net_pips={event['net_pips']}"
    with TRADE_SIGNAL_LOG_FILE.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def record_trade_marker(symbol, bucket_time, marker_info):
    if not marker_info or marker_info["price"] is None:
        return
    side = marker_info["side"]
    price = marker_info["price"]
    style = marker_info["style"]
    history = trade_marker_history[symbol][side][bucket_time][price]
    history.append(style)
    opening_price = first_prices[symbol][side].get(bucket_time)
    raw_count = price_data[symbol][side][price].get(bucket_time, 0)
    signed_count = raw_count
    if raw_count > 0 and opening_price is not None and price < opening_price:
        signed_count = -raw_count
    event = {
        "timestamp": marker_info.get("timestamp", bucket_time),
        "symbol": symbol,
        "side": side.upper(),
        "event": "OPEN" if style == "open" else "CLOSE",
        "bucket": bucket_time,
        "price": price,
        "signed_count": signed_count,
        "marker": render_plain_cell_value(signed_count, history),
        "state": marker_info.get("state", "UNKNOWN"),
        "entry_price": marker_info.get("entry_price"),
        "entry_timestamp": marker_info.get("entry_timestamp"),
        "net_pips": marker_info.get("net_pips"),
    }
    recent_trade_events.append(event)
    del recent_trade_events[:-MAX_TRADE_EVENT_LINES]
    append_trade_signal_log(event)


def visible_text(text):
    return ANSI_PATTERN.sub("", str(text))


def visible_len(text):
    return len(visible_text(text))


def pad_visible_right(text, width):
    raw = str(text)
    return (" " * max(0, width - visible_len(raw))) + raw


def render_plain_cell_value(signed_count, marker_history):
    text = str(signed_count)
    if marker_history:
        unique_styles = set(marker_history)
        if len(unique_styles) == 1:
            style = marker_history[0]
            count = len(marker_history)
            if style == "open":
                text = f"{'<' * count}{text}{'>' * count}"
            elif style == "close":
                text = f"{'>' * count}{text}{'<' * count}"
        else:
            segments = []
            for style in marker_history:
                if style == "open":
                    segments.append(f"<{text}>")
                elif style == "close":
                    segments.append(f">{text}<")
            text = "".join(segments) if segments else text
    return text


def format_colored_cell(signed_count, marker_history=None, pulse_target=False, pulse_phase=False, width=0):
    color = ANSI_GREEN if signed_count >= 0 else ANSI_RED
    rendered = pad_visible_right(render_plain_cell_value(signed_count, marker_history or []), width)
    if pulse_target:
        pulse_style = ANSI_BRIGHT if pulse_phase else ANSI_DIM
        return f"{pulse_style}{color}{rendered}{ANSI_RESET}"
    return f"{color}{rendered}{ANSI_RESET}"


def build_skill_summary_lines(symbol, current_bucket, previous_bucket=None):
    bid_metrics = compute_side_metrics(symbol, "bid", current_bucket)
    ask_metrics = compute_side_metrics(symbol, "ask", current_bucket)
    prior_open = first_prices[symbol]["bid"].get(previous_bucket) if previous_bucket else None
    current_open = bid_metrics["open"]
    state, key_transition, confirmation, open_move = classify_state(bid_metrics, ask_metrics, current_open, prior_open)

    lines = ["  Skill Read:", "    BID:"]
    lines.append(
        f"      Time={current_bucket} Open={format_open_price(bid_metrics['open'])} "
        f"Above={bid_metrics['above']} AtOpen={bid_metrics['at_open']} Below={bid_metrics['below']} Net={bid_metrics['net']}"
    )
    lines.append("    ASK:")
    lines.append(
        f"      Time={current_bucket} Open={format_open_price(ask_metrics['open'])} "
        f"Above={ask_metrics['above']} AtOpen={ask_metrics['at_open']} Below={ask_metrics['below']} Net={ask_metrics['net']}"
    )
    lines.append(f"    State: {state}")
    lines.append(f"    Key Transition: {key_transition}")
    if open_move is not None:
        lines.append(f"    Open Movement: {open_move}")
    lines.append(f"    Confirmation: {confirmation}")
    return lines, state


def build_trade_event_panel_lines():
    lines = ["Trade Signals", "-------------"]
    if not recent_trade_events:
        lines.append("No <> or >< events yet.")
        return lines

    for event in reversed(recent_trade_events[-MAX_TRADE_EVENT_LINES:]):
        lines.append(
            f"{event['timestamp']} {event['symbol']}"
        )
        lines.append(
            f"{event['event']} {event['side']} {event['marker']} @ {event['price']:.4f}"
        )
        lines.append(
            f"bucket={event['bucket']} state={event['state']}"
        )
        lines.append("")
    if lines[-1] == "":
        lines.pop()
    return lines


def print_two_panel(left_lines, right_lines):
    terminal_width = shutil.get_terminal_size((220, 40)).columns
    visible_left_width = max((visible_len(line) for line in left_lines), default=100)
    right_width = min(68, max((visible_len(line) for line in right_lines), default=24) + 2)
    spacer = "   "
    left_width = min(max(visible_left_width, 100), max(100, terminal_width - right_width - len(spacer)))

    total_lines = max(len(left_lines), len(right_lines))
    output_lines = []
    for index in range(total_lines):
        left = left_lines[index] if index < len(left_lines) else ""
        right = right_lines[index] if index < len(right_lines) else ""
        output_lines.append(f"{pad_visible_right(left, left_width)}{spacer}{right}")
    try:
        print("\n".join(output_lines))
        sys.stdout.flush()
    except OSError:
        pass


def display_frequency(pulse_phase=False):
    clear_screen()
    left_lines = [
        "--- Epic 016 GBP Price Frequency Analyzer (5-Min Buckets) ---",
        f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Source: {HTTP_SOURCE_URL}",
        "-" * 80,
    ]

    symbols = sorted(price_data.keys())
    recent_buckets = bucket_times[-MAX_COLUMNS:]
    current_bucket = recent_buckets[-1] if recent_buckets else None
    previous_bucket = recent_buckets[-2] if len(recent_buckets) > 1 else None

    for symbol in symbols:
        left_lines.append("")
        left_lines.append(f"[{symbol.upper()}]")
        if current_bucket:
            skill_lines, _ = build_skill_summary_lines(symbol, current_bucket, previous_bucket)
            left_lines.extend(skill_lines)
        for side in ["ask", "bid"]:
            left_lines.append("")
            left_lines.append(f"  {side.upper()} Cluster History:")
            opening_prices = first_prices[symbol][side]
            current_side_metrics = compute_side_metrics(symbol, side, current_bucket) if current_bucket else None
            all_prices = sorted(price_data[symbol][side].keys(), reverse=True)

            column_width = 6
            for bucket in recent_buckets:
                column_width = max(column_width, len(bucket))
                opening_price = opening_prices.get(bucket)
                if opening_price is not None:
                    column_width = max(column_width, len(f"{opening_price:.4f}"))
            for price in all_prices:
                for bucket in recent_buckets:
                    count = price_data[symbol][side][price].get(bucket, 0)
                    opening_price = opening_prices.get(bucket)
                    signed_count = count
                    if count > 0 and opening_price is not None and price < opening_price:
                        signed_count = -count
                    marker_history = trade_marker_history[symbol][side][bucket].get(price, [])
                    if count > 0 or marker_history:
                        column_width = max(
                            column_width,
                            visible_len(render_plain_cell_value(signed_count, marker_history)),
                        )

            header = f"    {'Price':<{PRICE_LABEL_WIDTH}}|" + "|".join(
                pad_visible_right(bucket, column_width) for bucket in recent_buckets
            )
            left_lines.append(header)
            left_lines.append("    " + "-" * len(header))

            open_row = f"    {'First Price':<{PRICE_LABEL_WIDTH}}|"
            open_row += "|".join(
                pad_visible_right(f"{opening_prices[bucket]:.4f}", column_width)
                if bucket in opening_prices
                else pad_visible_right("-", column_width)
                for bucket in recent_buckets
            )
            left_lines.append(open_row)

            for price in all_prices:
                row = f"    {price:.4f}".ljust(4 + PRICE_LABEL_WIDTH) + "|"
                has_data_in_view = False
                for bucket in recent_buckets:
                    count = price_data[symbol][side][price].get(bucket, 0)
                    opening_price = opening_prices.get(bucket)
                    signed_count = count
                    if count > 0 and opening_price is not None and price < opening_price:
                        signed_count = -count
                    marker_history = trade_marker_history[symbol][side][bucket].get(price, [])
                    pulse_target = False
                    if (
                        count > 0
                        and bucket == current_bucket
                        and opening_price is not None
                        and current_side_metrics is not None
                    ):
                        if current_side_metrics["net"] > 0 and price > opening_price:
                            pulse_target = True
                        elif current_side_metrics["net"] < 0 and price < opening_price:
                            pulse_target = True

                    cell = (
                        format_colored_cell(
                            signed_count,
                            marker_history,
                            pulse_target=pulse_target,
                            pulse_phase=pulse_phase,
                            width=column_width,
                        )
                        if count > 0
                        else (
                            pad_visible_right("-", column_width)
                            if not marker_history
                            else format_colored_cell(
                                0,
                                marker_history,
                                pulse_target=False,
                                pulse_phase=pulse_phase,
                                width=column_width,
                            )
                        )
                    )
                    row += f"{cell}|"
                    if count > 0:
                        has_data_in_view = True
                    elif marker_history:
                        has_data_in_view = True

                if has_data_in_view:
                    left_lines.append(row)
    print_two_panel(left_lines, build_trade_event_panel_lines())


def run_analyzer():
    global last_timestamp_str, bucket_times, last_pulse_phase, last_trade_state_by_symbol, last_snapshot_time
    print(f"Starting Epic 016 GBP analyzer on {HTTP_SOURCE_URL}...")
    print(f"Snapshots will be saved to: {GENERATED_DATA_ROOT / 'TradeApps' / 'breakout' / 'fs' / 'json' / 'live' / 'forex'}")

    try:
        while True:
            should_render = False
            try:
                quotes = fetch_quotes()
                if not quotes:
                    time.sleep(POLL_INTERVAL)
                    continue

                ts_str = max((quote.get("timestamp") or "") for quote in quotes)

                for quote in quotes:
                    symbol = (quote.get("code") or "").upper()
                    if symbol:
                        bid = quote.get("bid")
                        ask = quote.get("ask")
                        if bid is not None and ask is not None:
                            last_raw_prices[symbol] = {"bid": round(float(bid), 5), "ask": round(float(ask), 5)}

                if ts_str != last_timestamp_str:
                    dt = parse_quote_timestamp(ts_str)
                    bucket_time = get_bucket_time(dt)
                    if bucket_time not in bucket_times:
                        bucket_times.append(bucket_time)
                        bucket_times = sorted(bucket_times)

                    for quote in quotes:
                        symbol = (quote.get("code") or "").upper()
                        if not is_gbp_symbol(symbol):
                            continue

                        for side in ["bid", "ask"]:
                            val_raw = quote.get(side)
                            if val_raw is not None:
                                price_pip = round(float(val_raw), 4)
                                if bucket_time not in first_prices[symbol][side]:
                                    first_prices[symbol][side][bucket_time] = price_pip
                                price_data[symbol][side][price_pip][bucket_time] += 1

                    active_symbols = sorted(
                        symbol
                        for symbol in { (quote.get("code") or "").upper() for quote in quotes }
                        if is_gbp_symbol(symbol)
                    )
                    previous_bucket = bucket_times[-2] if len(bucket_times) > 1 else None
                    for symbol in active_symbols:
                        marker_info = get_bucket_marker(symbol, bucket_time, previous_bucket)
                        current_trade_state = marker_info["state"] if marker_info else None
                        if marker_info and last_trade_state_by_symbol.get(symbol) != current_trade_state:
                            marker_info["timestamp"] = ts_str
                            if should_record_trade_event(symbol, marker_info):
                                record_trade_marker(symbol, bucket_time, marker_info)
                        last_trade_state_by_symbol[symbol] = current_trade_state

                    last_timestamp_str = ts_str
                    should_render = True

            except (json.JSONDecodeError, OSError, TimeoutError, ValueError):
                pass

            pulse_phase = int(time.time() * 2) % 2
            if price_data and last_pulse_phase != pulse_phase:
                should_render = True
            if should_render and price_data:
                display_frequency(pulse_phase=bool(pulse_phase))
            last_pulse_phase = pulse_phase

            if (time.time() - last_snapshot_time) >= SNAPSHOT_INTERVAL_SECONDS:
                capture_snapshot()

            time.sleep(POLL_INTERVAL)

    except KeyboardInterrupt:
        print("\nAnalyzer stopped.")


if __name__ == "__main__":
    run_analyzer()
