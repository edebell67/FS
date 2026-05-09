from __future__ import annotations

import argparse
import json
from datetime import datetime
from typing import Any, Dict, List, Optional

from common import (
    BaseBreakoutStrategy,
    COMMISSION_PIPS,
    DEFAULT_TRADE_PRODUCTS,
    POLL_INTERVAL_SECONDS,
    SPREAD_PIPS,
    _LATEST_TRADING_DATE,
    _ensure_json_ext,
    _increment_global_active,
    _load_config,
    _resolve_day_directory,
    _safe_float,
    _strip_trade_status_suffix,
    _trading_date_string,
    _with_trade_status_suffix,
    run_multiwindow,
)


DEFAULT_MOMENTUM_STEP_PIPS = 5.0
DEFAULT_TP_PIPS = 5.0
DEFAULT_SL_PIPS = 7.0


class MomentumStrategy(BaseBreakoutStrategy):
    """Directional momentum ladder that supports multiple simultaneous positions."""

    allow_reversal = True

    def __init__(
        self,
        window_size: int,
        pip_buffer: float,
        tp_pips: float,
        sl_pips: float,
        commission_pips: float,
        spread_pips: float,
        trade_product: str,
        script_name: str,
        max_live_trades: Optional[int] = None,
    ) -> None:
        self.open_trades: List[Dict[str, Any]] = []
        self.anchor_price: Optional[float] = None
        self.initial_dual_entry_done = False
        self.last_open_price_by_direction: Dict[str, Optional[float]] = {
            "LONG": None,
            "SHORT": None,
        }
        super().__init__(
            window_size=window_size,
            pip_buffer=pip_buffer,
            tp_pips=tp_pips,
            sl_pips=sl_pips,
            commission_pips=commission_pips,
            spread_pips=spread_pips,
            trade_product=trade_product,
            script_name=script_name,
            max_live_trades=max_live_trades,
        )
        self.open_trade = None
        self._refresh_directional_levels()

    @property
    def step_pips(self) -> float:
        return float(self.pip_buffer)

    @property
    def step_price_distance(self) -> float:
        return self.step_pips / self.pip_multiplier

    def _load_persisted_state(self) -> None:
        if not self.state_persistence:
            print(f"[INFO] State persistence disabled for {self.trade_product} ({self.script_name}). Starting fresh.")
            self.open_trades = []
            self.open_trade = None
            return

        current_params = f"{self.window_size}_{self.pip_buffer}_{self.tp_pips}_{self.sl_pips}"
        max_id = 0
        restored_trades: List[Dict[str, Any]] = []
        today_str = _LATEST_TRADING_DATE or datetime.now().strftime("%Y-%m-%d")
        folder_path = _resolve_day_directory(self.run_mode.lower(), today_str, self.trade_product)

        if folder_path.exists():
            for json_path in folder_path.glob("*_op.json"):
                try:
                    if json_path.stat().st_size == 0 or json_path.name.startswith("_"):
                        continue

                    with json_path.open("r", encoding="utf-8") as handle:
                        data = json.load(handle)

                    trade_id = data.get("trade_id", 0)
                    if isinstance(trade_id, str) and trade_id.isdigit():
                        trade_id = int(trade_id)
                    elif not isinstance(trade_id, (int, float)):
                        trade_id = 0
                    max_id = max(max_id, int(trade_id))

                    filename = _ensure_json_ext(json_path.name)
                    base_filename = _strip_trade_status_suffix(filename)
                    if (
                        data.get("status") == "OPEN"
                        and data.get("product", "").upper() == self.trade_product
                        and (self.script_name in filename or data.get("script_name") == self.script_name)
                        and current_params in filename
                        and data.get("window_size") == self.window_size
                    ):
                        normalized_name = _with_trade_status_suffix(base_filename, "OPEN")
                        if filename != normalized_name:
                            try:
                                new_path = json_path.with_name(normalized_name)
                                json_path.rename(new_path)
                                json_path = new_path
                                filename = normalized_name
                            except OSError as exc:
                                print(f"[PERSIST] Failed to normalize {json_path.name}: {exc}")

                        data["json_base_filename"] = base_filename
                        data["json_filename"] = filename
                        data["entry_time"] = self._coerce_timestamp(data.get("entry_time"))
                        data["id"] = data.get("trade_id", trade_id)
                        restored_trades.append(data)
                        print(f"[PERSIST] Restored open trade #{data.get('trade_id')} from {filename}")
                except Exception as exc:
                    print(f"[PERSIST] Error reading {json_path.name}: {exc}")

        restored_trades.sort(key=lambda trade: int(trade.get("trade_id", 0)))
        self.trade_counter = max_id
        self.open_trades = restored_trades
        self.open_trade = None
        for trade in self.open_trades:
            _increment_global_active(self.trade_product, trade.get("direction", ""))
        self.initial_dual_entry_done = bool(self.open_trades)

        if self.open_trades:
            print(
                f"[RESUME] Restored {len(self.open_trades)} open trade(s) for "
                f"{self.trade_product} ({self.script_name}). Counter restored to {max_id}."
            )
        else:
            print(f"[INFO] No open trades found for {self.trade_product} ({self.script_name}). Counter restored to {max_id}.")

    def _refresh_directional_levels(self) -> None:
        self.last_open_price_by_direction = {"LONG": None, "SHORT": None}
        for direction in ("LONG", "SHORT"):
            same_direction = [
                trade
                for trade in self.open_trades
                if str(trade.get("direction", "")).upper() == direction
            ]
            if same_direction:
                latest_trade = max(same_direction, key=lambda trade: int(trade.get("id", trade.get("trade_id", 0))))
                self.last_open_price_by_direction[direction] = float(latest_trade["entry_price"])

    def _maybe_initialize_anchor(self, current_price: float) -> None:
        if self.anchor_price is None:
            self.anchor_price = current_price
            print(
                f"[{datetime.now()}] [MOMENTUM-ANCHOR] "
                f"{self.trade_product} anchor set to {self.anchor_price:.5f}"
            )

    def _bootstrap_initial_dual_entry(self, current_time: Any, current_price: float) -> set[str]:
        if self.initial_dual_entry_done:
            return set()

        opened_directions: set[str] = set()
        existing_directions = {
            str(trade.get("direction", "")).upper()
            for trade in self.open_trades
        }
        for direction in ("LONG", "SHORT"):
            if direction in existing_directions:
                continue
            if self._enter_momentum_trade(current_time, current_price, direction):
                opened_directions.add(direction)

        if opened_directions:
            print(
                f"[{datetime.now()}] [MOMENTUM-BOOTSTRAP] "
                f"Opened initial {sorted(opened_directions)} trades for {self.trade_product} at {current_price:.5f}"
            )
        self.initial_dual_entry_done = True
        return opened_directions

    def _enter_momentum_trade(self, current_time: Any, entry_price: float, direction: str) -> bool:
        prior_trade = self.open_trade
        self.open_trade = None
        super().enter_trade(current_time, entry_price, direction)
        new_trade = self.open_trade
        self.open_trade = prior_trade

        if not new_trade:
            return False

        self.open_trades.append(new_trade)
        self.open_trades.sort(key=lambda trade: int(trade.get("id", 0)))
        self._refresh_directional_levels()
        return True

    def _close_trade_record(self, trade: Dict[str, Any], current_time: Any, exit_price: float, reason: str) -> bool:
        self.open_trade = trade
        was_closed = super().close_trade(current_time, exit_price, reason)
        self.open_trade = None
        if was_closed:
            self.open_trades = [item for item in self.open_trades if item.get("id") != trade.get("id")]
            self._refresh_directional_levels()
        return was_closed

    def _close_all_open_trades(self, current_time: Any, current_price: float, reason: str) -> None:
        for trade in list(self.open_trades):
            self._close_trade_record(trade, current_time, current_price, reason)

    def _force_close_prior_trading_day(self, current_time: Any, current_price: float) -> bool:
        current_date = _trading_date_string(current_time)
        if not current_date:
            return False

        prior_trades = [
            trade
            for trade in self.open_trades
            if (_trading_date_string(trade.get("entry_time")) or current_date) < current_date
        ]
        if not prior_trades:
            return False

        print(
            f"[{datetime.now()}] [DATE-ROLLOVER-FORCE-CLOSE] Closing {len(prior_trades)} "
            f"momentum trade(s) for {self.trade_product} before processing {current_date}."
        )
        for trade in list(prior_trades):
            self._close_trade_record(trade, current_time, current_price, "Date Rollover Force Close")

        self.anchor_price = None
        self.initial_dual_entry_done = bool(self.open_trades)
        self.price_history.clear()
        self._refresh_directional_levels()
        return True

    def _save_and_update_open_trades(self, current_time: Any, current_price: float) -> None:
        for trade in self.open_trades:
            self.open_trade = trade
            self._check_immediate_live_activation(current_time, current_price)
            self._check_grid_live_toggle(current_time, current_price)
            self._save_trade_json(current_price)
        self.open_trade = None

    def _check_all_exits(
        self,
        current_time: Any,
        current_price: float,
        *,
        include_tp: bool,
        include_sl: bool,
        skip_tp_directions: Optional[set[str]] = None,
    ) -> bool:
        closed_any = False
        tp_skip = skip_tp_directions or set()
        for trade in list(self.open_trades):
            direction = str(trade.get("direction", "")).upper()
            entry_price = float(trade["entry_price"])
            if direction == "LONG":
                tp_level = entry_price + (self.tp_pips / self.pip_multiplier)
                sl_level = entry_price - (self.sl_pips / self.pip_multiplier)
                if include_tp and direction not in tp_skip and current_price >= tp_level:
                    closed_any = self._close_trade_record(trade, current_time, tp_level, "TP Hit") or closed_any
                    continue
                if include_sl and current_price <= sl_level:
                    closed_any = self._close_trade_record(trade, current_time, sl_level, "SL Hit") or closed_any
                    continue
            elif direction == "SHORT":
                tp_level = entry_price - (self.tp_pips / self.pip_multiplier)
                sl_level = entry_price + (self.sl_pips / self.pip_multiplier)
                if include_tp and direction not in tp_skip and current_price <= tp_level:
                    closed_any = self._close_trade_record(trade, current_time, tp_level, "TP Hit") or closed_any
                    continue
                if include_sl and current_price >= sl_level:
                    closed_any = self._close_trade_record(trade, current_time, sl_level, "SL Hit") or closed_any
                    continue
        return closed_any

    def _log_open_trade_summary(self, current_price: float) -> None:
        long_count = sum(1 for trade in self.open_trades if trade.get("direction") == "LONG")
        short_count = sum(1 for trade in self.open_trades if trade.get("direction") == "SHORT")
        anchor_value = self.anchor_price if self.anchor_price is not None else current_price
        print(
            f"[{datetime.now()}] [MOMENTUM] {self.trade_product} price={current_price:.5f} "
            f"anchor={anchor_value:.5f} "
            f"open_long={long_count} open_short={short_count} "
            f"last_long={self.last_open_price_by_direction['LONG']} "
            f"last_short={self.last_open_price_by_direction['SHORT']}"
        )

    def check_and_enter(self, current_time, current_price):
        if self.anchor_price is None:
            return set()

        step = self.step_price_distance
        long_reference = self.last_open_price_by_direction["LONG"]
        short_reference = self.last_open_price_by_direction["SHORT"]
        opened_directions: set[str] = set()

        long_threshold = (long_reference if long_reference is not None else self.anchor_price) + step
        short_threshold = (short_reference if short_reference is not None else self.anchor_price) - step

        while current_price >= long_threshold:
            self._audit_signal_event(
                "momentum_detected",
                current_time=current_time,
                signal="LONG",
                price=current_price,
                threshold=long_threshold,
                step_pips=self.step_pips,
            )
            if not self._enter_momentum_trade(current_time, long_threshold, "LONG"):
                break
            opened_directions.add("LONG")
            long_reference = self.last_open_price_by_direction["LONG"]
            long_threshold = (long_reference if long_reference is not None else self.anchor_price) + step

        while current_price <= short_threshold:
            self._audit_signal_event(
                "momentum_detected",
                current_time=current_time,
                signal="SHORT",
                price=current_price,
                threshold=short_threshold,
                step_pips=self.step_pips,
            )
            if not self._enter_momentum_trade(current_time, short_threshold, "SHORT"):
                break
            opened_directions.add("SHORT")
            short_reference = self.last_open_price_by_direction["SHORT"]
            short_threshold = (short_reference if short_reference is not None else self.anchor_price) - step

        return opened_directions

    def process_new_tick(self, timestamp_value: Any, price: Any, bid: Any = None, ask: Any = None) -> None:
        current_time = self._coerce_timestamp(timestamp_value)
        current_price = _safe_float(price)
        self.latest_bid = _safe_float(bid)
        self.latest_ask = _safe_float(ask)

        if current_time is None or current_price is None:
            return

        self._force_close_prior_trading_day(current_time, current_price)
        self._maybe_initialize_anchor(current_price)
        self._check_all_exits(current_time, current_price, include_tp=False, include_sl=True)

        if self.is_eod(current_time):
            if self.open_trades:
                print(
                    f"[{datetime.now()}] [EOD-FORCE-CLOSE] Closing {len(self.open_trades)} "
                    f"momentum trade(s) for {self.trade_product}."
                )
                self._close_all_open_trades(current_time, current_price, "EOD Force Close")
            return

        opened_directions = self._bootstrap_initial_dual_entry(current_time, current_price)
        opened_directions.update(self.check_and_enter(current_time, current_price))
        self._check_all_exits(
            current_time,
            current_price,
            include_tp=True,
            include_sl=False,
            skip_tp_directions=opened_directions,
        )
        if self.open_trades:
            self._save_and_update_open_trades(current_time, current_price)
            self._log_open_trade_summary(current_price)

        self.price_history.append(current_price)


def _default_momentum_step_pips() -> float:
    config = _load_config()
    return float(config.get("momentum_step_pips", DEFAULT_MOMENTUM_STEP_PIPS))


def build_momentum_script_alias(tp_pips: float, sl_pips: float) -> str:
    return f"momentum_0_tp{float(tp_pips):.1f}_sl{float(sl_pips):.1f}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Live momentum trading loop for FX quotes.")
    parser.add_argument("--poll-interval", type=int, default=POLL_INTERVAL_SECONDS, help="Seconds between quote fetches.")
    parser.add_argument("--window-size", type=int, default=1, help="Anchor window for the first recorded price.")
    parser.add_argument(
        "--step-pips",
        type=float,
        default=_default_momentum_step_pips(),
        help="Distance in pips between momentum entries.",
    )
    parser.add_argument("--tp-pips", type=float, default=DEFAULT_TP_PIPS)
    parser.add_argument("--sl-pips", type=float, default=DEFAULT_SL_PIPS)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_multiwindow(
        MomentumStrategy,
        trade_products=DEFAULT_TRADE_PRODUCTS,
        poll_interval_seconds=args.poll_interval,
        window_override=args.window_size,
        pip_buffer=args.step_pips,
        tp_pips=args.tp_pips,
        sl_pips=args.sl_pips,
        commission_pips=COMMISSION_PIPS,
        spread_pips=SPREAD_PIPS,
        script_alias=build_momentum_script_alias(args.tp_pips, args.sl_pips),
    )
