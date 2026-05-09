from __future__ import annotations

import argparse
from datetime import datetime
from typing import Any, Dict, Optional

from common import (
    COMMISSION_PIPS,
    DEFAULT_TRADE_PRODUCTS,
    POLL_INTERVAL_SECONDS,
    SPREAD_PIPS,
    _load_config,
    run_multiwindow,
)
from momentum import (
    DEFAULT_MOMENTUM_STEP_PIPS,
    DEFAULT_SL_PIPS,
    DEFAULT_TP_PIPS,
    MomentumStrategy,
)


REVERSE_SIGNAL_DIRECTION = {
    "LONG": "SHORT",
    "SHORT": "LONG",
}


class MomentumReverseStrategy(MomentumStrategy):
    """Momentum ladder variant that reverses generated signals before trade entry."""

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
        self.last_open_price_by_signal: Dict[str, Optional[float]] = {
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

    def _signal_for_trade(self, trade: Dict[str, Any]) -> str:
        signal = str(trade.get("momentum_signal") or "").upper()
        if signal in REVERSE_SIGNAL_DIRECTION:
            return signal
        direction = str(trade.get("direction", "")).upper()
        return REVERSE_SIGNAL_DIRECTION.get(direction, "")

    def _refresh_directional_levels(self) -> None:
        super()._refresh_directional_levels()
        self.last_open_price_by_signal = {"LONG": None, "SHORT": None}
        for signal in ("LONG", "SHORT"):
            same_signal = [
                trade
                for trade in self.open_trades
                if self._signal_for_trade(trade) == signal
            ]
            if same_signal:
                latest_trade = max(same_signal, key=lambda trade: int(trade.get("id", trade.get("trade_id", 0))))
                self.last_open_price_by_signal[signal] = float(latest_trade["entry_price"])

    def _enter_reverse_momentum_trade(self, current_time: Any, entry_price: float, signal_direction: str) -> bool:
        signal = str(signal_direction or "").upper()
        trade_direction = REVERSE_SIGNAL_DIRECTION.get(signal)
        if not trade_direction:
            return False

        if not self._enter_momentum_trade(current_time, entry_price, trade_direction):
            return False

        new_trade = max(self.open_trades, key=lambda trade: int(trade.get("id", trade.get("trade_id", 0))))
        new_trade["momentum_signal"] = signal
        new_trade["reversed_from_signal"] = True

        # Persist reverse metadata because enter_trade saves once before this variant annotates the trade.
        prior_trade = self.open_trade
        self.open_trade = new_trade
        self._save_trade_json(entry_price)
        self.open_trade = prior_trade
        self._refresh_directional_levels()
        return True

    def _bootstrap_initial_dual_entry(self, current_time: Any, current_price: float) -> set[str]:
        if self.initial_dual_entry_done:
            return set()

        opened_directions: set[str] = set()
        existing_signals = {
            self._signal_for_trade(trade)
            for trade in self.open_trades
        }
        for signal in ("LONG", "SHORT"):
            if signal in existing_signals:
                continue
            if self._enter_reverse_momentum_trade(current_time, current_price, signal):
                opened_directions.add(REVERSE_SIGNAL_DIRECTION[signal])

        if opened_directions:
            print(
                f"[{datetime.now()}] [MOMENTUM-R-BOOTSTRAP] "
                f"Opened initial reversed {sorted(opened_directions)} trades for {self.trade_product} at {current_price:.5f}"
            )
        self.initial_dual_entry_done = True
        return opened_directions

    def _log_open_trade_summary(self, current_price: float) -> None:
        long_count = sum(1 for trade in self.open_trades if trade.get("direction") == "LONG")
        short_count = sum(1 for trade in self.open_trades if trade.get("direction") == "SHORT")
        anchor_value = self.anchor_price if self.anchor_price is not None else current_price
        print(
            f"[{datetime.now()}] [MOMENTUM-R] {self.trade_product} price={current_price:.5f} "
            f"anchor={anchor_value:.5f} "
            f"open_long={long_count} open_short={short_count} "
            f"last_long_signal={self.last_open_price_by_signal['LONG']} "
            f"last_short_signal={self.last_open_price_by_signal['SHORT']}"
        )

    def check_and_enter(self, current_time, current_price):
        if self.anchor_price is None:
            return set()

        step = self.step_price_distance
        long_signal_reference = self.last_open_price_by_signal["LONG"]
        short_signal_reference = self.last_open_price_by_signal["SHORT"]
        opened_directions: set[str] = set()

        long_threshold = (long_signal_reference if long_signal_reference is not None else self.anchor_price) + step
        short_threshold = (short_signal_reference if short_signal_reference is not None else self.anchor_price) - step

        while current_price >= long_threshold:
            self._audit_signal_event(
                "momentum_reverse_detected",
                current_time=current_time,
                signal="LONG",
                reversed_to="SHORT",
                price=current_price,
                threshold=long_threshold,
                step_pips=self.step_pips,
            )
            if not self._enter_reverse_momentum_trade(current_time, long_threshold, "LONG"):
                break
            opened_directions.add("SHORT")
            long_signal_reference = self.last_open_price_by_signal["LONG"]
            long_threshold = (long_signal_reference if long_signal_reference is not None else self.anchor_price) + step

        while current_price <= short_threshold:
            self._audit_signal_event(
                "momentum_reverse_detected",
                current_time=current_time,
                signal="SHORT",
                reversed_to="LONG",
                price=current_price,
                threshold=short_threshold,
                step_pips=self.step_pips,
            )
            if not self._enter_reverse_momentum_trade(current_time, short_threshold, "SHORT"):
                break
            opened_directions.add("LONG")
            short_signal_reference = self.last_open_price_by_signal["SHORT"]
            short_threshold = (short_signal_reference if short_signal_reference is not None else self.anchor_price) - step

        return opened_directions


def _default_momentum_step_pips() -> float:
    config = _load_config()
    return float(config.get("momentum_step_pips", DEFAULT_MOMENTUM_STEP_PIPS))


def build_momentum_reverse_script_alias(tp_pips: float, sl_pips: float) -> str:
    return f"momentum_r_0_tp{float(tp_pips):.1f}_sl{float(sl_pips):.1f}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Live reverse-momentum trading loop for FX quotes.")
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
        MomentumReverseStrategy,
        trade_products=DEFAULT_TRADE_PRODUCTS,
        poll_interval_seconds=args.poll_interval,
        window_override=args.window_size,
        pip_buffer=args.step_pips,
        tp_pips=args.tp_pips,
        sl_pips=args.sl_pips,
        commission_pips=COMMISSION_PIPS,
        spread_pips=SPREAD_PIPS,
        script_alias=build_momentum_reverse_script_alias(args.tp_pips, args.sl_pips),
    )
