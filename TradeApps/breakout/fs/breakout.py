from __future__ import annotations

import argparse

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
)


class BreakoutStrategy(BaseBreakoutStrategy):
    """Standard breakout: wait for window, enter on threshold breach."""

    def check_and_enter(self, current_time, current_price):
        """Check for a breakout and enter a trade."""
        if len(self.price_history) < self.window_size:
            return

        # Ensure we don't trade against ourselves if reversals are not allowed.
        if self.open_trade and not self.allow_reversal:
            return

        min_price = min(self.price_history)
        max_price = max(self.price_history)

        long_threshold = max_price + self.pip_buffer
        short_threshold = min_price - self.pip_buffer

        if current_price > long_threshold:
            self._audit_signal_event(
                'breakout_detected', current_time,
                signal='LONG', price=current_price,
                long_threshold=long_threshold, short_threshold=short_threshold,
            )
            self.enter_trade(current_time, current_price, 'LONG')
        elif current_price < short_threshold:
            self._audit_signal_event(
                'breakout_detected', current_time,
                signal='SHORT', price=current_price,
                long_threshold=long_threshold, short_threshold=short_threshold,
            )
            self.enter_trade(current_time, current_price, 'SHORT')


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Live breakout trading loop for FX quotes.')
    parser.add_argument('--poll-interval', type=int, default=POLL_INTERVAL_SECONDS, help='Seconds between quote fetches.')
    parser.add_argument('--window-size', type=int, default=None, help='Optional override window size.')
    parser.add_argument('--pip-buffer', type=float, default=PIP_BUFFER)
    parser.add_argument('--tp-pips', type=float, default=None)
    parser.add_argument('--sl-pips', type=float, default=None)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    run_multiwindow(
        BreakoutStrategy,
        trade_products=DEFAULT_TRADE_PRODUCTS,
        poll_interval_seconds=args.poll_interval,
        window_override=args.window_size,
        pip_buffer=args.pip_buffer,
        tp_pips=args.tp_pips,
        sl_pips=args.sl_pips,
        commission_pips=COMMISSION_PIPS,
        spread_pips=SPREAD_PIPS,
        script_alias='breakout',
    )
