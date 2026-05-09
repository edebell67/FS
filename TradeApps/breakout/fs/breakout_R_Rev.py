from __future__ import annotations

import argparse
from datetime import datetime

from common import (
    BaseBreakoutStrategy,
    DEFAULT_TRADE_PRODUCTS,
    POLL_INTERVAL_SECONDS,
    PIP_BUFFER,
    TP_PIPS,
    SL_PIPS,
    COMMISSION_PIPS,
    SPREAD_PIPS,
    run_multiwindow,
    _safe_float,
)


class BreakoutReversalContrarianStrategy(BaseBreakoutStrategy):
    allow_reversal = True

    def check_and_enter(self, current_time, current_price):
        if len(self.price_history) < self.window_size:
            return
        max_history = max(self.price_history)
        min_history = min(self.price_history)
        long_threshold = max_history + self.pip_buffer
        short_threshold = min_history - self.pip_buffer
        signal = None
        if current_price > long_threshold:
            signal = 'SHORT'
        elif current_price < short_threshold:
            signal = 'LONG'
        if signal:
            self._audit_signal_event(
                'breakout_detected', current_time,
                signal=signal, price=current_price,
                long_threshold=long_threshold, short_threshold=short_threshold,
            )
            if self.open_trade and self.open_trade['direction'] != signal:
                print(f"*** REVERSING POSITION *** from {self.open_trade['direction']} to {signal}")
                self.close_trade(current_time, current_price, 'Reversed')
            if not self.open_trade:
                self.enter_trade(current_time, current_price, signal)

    def process_new_tick(self, timestamp_str, price, bid=None, ask=None):
        current_time = self._coerce_timestamp(timestamp_str)
        current_price = _safe_float(price)
        self.latest_bid = _safe_float(bid)
        self.latest_ask = _safe_float(ask)
        if current_time is None or current_price is None:
            return

        window_ready = len(self.price_history) >= self.window_size

        # 1. Check for TP/SL exits first
        self.check_and_exit(current_time, current_price)

        # 2. EOD force-close if past 23:00
        if self.open_trade and self.is_eod(current_time):
            print(f"[{datetime.now()}] [EOD-FORCE-CLOSE] Closing {self.trade_product} trade #{self.open_trade['id']} - Past 23:00 cutoff.")
            self.close_trade(current_time, current_price, 'EOD Force Close')
            self.price_history.append(current_price)
            return

        # 3. Window full - check entry/reversal; skip new entries after EOD
        if window_ready and not self.is_eod(current_time):
            self.check_and_enter(current_time, current_price)

        # 3. Display status if trade open
        if self.open_trade:
            self._check_immediate_live_activation(current_time, current_price)
            self._check_grid_live_toggle(current_time, current_price)
            self.display_open_trade_status(current_price)

        self.price_history.append(current_price)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Live breakout contrarian reversal strategy.')
    parser.add_argument('--poll-interval', type=int, default=POLL_INTERVAL_SECONDS)
    parser.add_argument('--window-size', type=int, default=None)
    parser.add_argument('--pip-buffer', type=float, default=PIP_BUFFER)
    parser.add_argument('--tp-pips', type=float, default=None)
    parser.add_argument('--sl-pips', type=float, default=None)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    print(f"[DEBUG-STARTUP] args.window_size={args.window_size}, type={type(args.window_size)}")
    run_multiwindow(
        BreakoutReversalContrarianStrategy,
        trade_products=DEFAULT_TRADE_PRODUCTS,
        poll_interval_seconds=args.poll_interval,
        window_override=args.window_size,
        pip_buffer=args.pip_buffer,
        tp_pips=args.tp_pips,
        sl_pips=args.sl_pips,
        commission_pips=COMMISSION_PIPS,
        spread_pips=SPREAD_PIPS,
        script_alias='breakout_R_Rev',
    )
