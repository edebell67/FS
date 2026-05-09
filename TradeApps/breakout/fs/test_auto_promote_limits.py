import sys
from datetime import datetime
from pathlib import Path


FS_DIR = Path(__file__).resolve().parent
if str(FS_DIR) not in sys.path:
    sys.path.insert(0, str(FS_DIR))

import common


def _stub_contract(product, config):
    return {
        "symbol": product,
        "secType": "CASH",
        "exchange": "IDEALPRO",
        "currency": "USD",
    }


def _build_strategy_for_auto_promote(monkeypatch):
    strategy = common.BaseBreakoutStrategy.__new__(common.BaseBreakoutStrategy)
    strategy.script_name = "breakout_demo"
    strategy.trade_product = "EURUSD"
    strategy.run_mode = "LIVE"
    strategy.window_size = 2
    strategy.pip_buffer = 0.00015
    strategy.tp_pips = 30.0
    strategy.sl_pips = 5.0
    strategy.latest_bid = 1.0999
    strategy.latest_ask = 1.1001
    strategy.l_trade_generation_mode = "both"
    strategy.profitability_guard_config = {}
    strategy.open_trade = {
        "id": "trade-123",
        "entry_time": datetime(2026, 4, 10, 9, 15, 0),
        "source_screen": "breakout",
        "source_group": "breakout",
        "live_cap_group": "breakout",
    }
    monkeypatch.setattr(
        common.BaseBreakoutStrategy,
        "_is_market_bias_entry_allowed",
        lambda self, direction, timestamp=None: (True, ""),
    )
    monkeypatch.setattr(
        common.BaseBreakoutStrategy,
        "_is_auto_promote_active",
        lambda self, direction, mode: mode == "net",
    )
    monkeypatch.setattr(
        common.BaseBreakoutStrategy,
        "_is_active",
        lambda self, direction, mode: False,
    )
    monkeypatch.setattr(
        common.BaseBreakoutStrategy,
        "_is_profitability_guard_passed",
        lambda self, direction, mode: False,
    )
    monkeypatch.setattr(common, "_load_config", lambda: {})
    monkeypatch.setattr(common, "_get_grid_live_origin", lambda *_: {"source": None, "group": None})
    monkeypatch.setattr(common, "_get_grid_live_context_snapshot", lambda *_: {})
    monkeypatch.setattr(common.BaseBreakoutStrategy, "_save_trade_json", lambda self, current_price: None)
    return strategy


def test_auto_promote_bypasses_daily_target_but_still_writes_order(tmp_path, monkeypatch):
    monkeypatch.setattr(
        common,
        "_load_config",
        lambda: {
            "archive": False,
            "run_mode": "LIVE",
            "daily_target": 100.0,
            "max_live_trades": 3,
            "max_trades_to_tws": 3,
            "send_json_files": str(tmp_path),
        },
    )
    monkeypatch.setattr(common, "_get_total_open_live_trades_for_group", lambda *_: 0)
    monkeypatch.setattr(common, "_get_group_closed_live_pnl", lambda *_: 250.0)
    monkeypatch.setattr(common, "_get_total_open_tws_sent_trades", lambda *_: 0)
    monkeypatch.setattr(common, "_get_tws_contract_details", _stub_contract)
    monkeypatch.setattr(common, "_trade_quantity_for_product", lambda *_: 1000)
    monkeypatch.setattr(common, "_resolve_product_type", lambda *_: "forex")
    monkeypatch.setattr(common, "_increment_global_active", lambda *_: None)
    common._LIVE_ORDERS_SENT_MEMORY_CACHE.clear()

    path = common._create_l_trade_order(
        product="EURUSD",
        direction="LONG",
        strategy_key="breakout_demo",
        trade_id="trade-1",
        current_price=1.1,
        mode="net",
        source_group="breakout",
        is_auto_promote=True,
    )

    assert path is not None
    assert Path(path).exists()
    assert common._LAST_L_TRADE_ORDER_ERROR is None


def test_auto_promote_still_respects_max_live_trades_limit(tmp_path, monkeypatch):
    monkeypatch.setattr(
        common,
        "_load_config",
        lambda: {
            "archive": False,
            "run_mode": "LIVE",
            "daily_target": 100.0,
            "max_live_trades": 1,
            "max_trades_to_tws": 3,
            "send_json_files": str(tmp_path),
        },
    )
    monkeypatch.setattr(common, "_get_total_open_live_trades_for_group", lambda *_: 1)
    monkeypatch.setattr(common, "_get_group_closed_live_pnl", lambda *_: 0.0)
    monkeypatch.setattr(common, "_get_total_open_tws_sent_trades", lambda *_: 0)
    monkeypatch.setattr(common, "_get_tws_contract_details", _stub_contract)
    monkeypatch.setattr(common, "_trade_quantity_for_product", lambda *_: 1000)
    monkeypatch.setattr(common, "_resolve_product_type", lambda *_: "forex")
    monkeypatch.setattr(common, "_increment_global_active", lambda *_: None)
    common._LIVE_ORDERS_SENT_MEMORY_CACHE.clear()

    path = common._create_l_trade_order(
        product="EURUSD",
        direction="LONG",
        strategy_key="breakout_demo",
        trade_id="trade-2",
        current_price=1.1,
        mode="net",
        source_group="breakout",
        is_auto_promote=True,
    )

    assert path is None
    assert "max_live_trades reached" in (common._LAST_L_TRADE_ORDER_ERROR or "")


def test_auto_promote_still_respects_tws_limit(tmp_path, monkeypatch):
    monkeypatch.setattr(
        common,
        "_load_config",
        lambda: {
            "archive": False,
            "run_mode": "LIVE",
            "daily_target": 100.0,
            "max_live_trades": 3,
            "max_trades_to_tws": 1,
            "send_json_files": str(tmp_path),
        },
    )
    monkeypatch.setattr(common, "_get_total_open_live_trades_for_group", lambda *_: 0)
    monkeypatch.setattr(common, "_get_group_closed_live_pnl", lambda *_: 0.0)
    monkeypatch.setattr(common, "_get_total_open_tws_sent_trades", lambda *_: 1)
    monkeypatch.setattr(common, "_get_tws_contract_details", _stub_contract)
    monkeypatch.setattr(common, "_trade_quantity_for_product", lambda *_: 1000)
    monkeypatch.setattr(common, "_resolve_product_type", lambda *_: "forex")
    monkeypatch.setattr(common, "_increment_global_active", lambda *_: None)
    common._LIVE_ORDERS_SENT_MEMORY_CACHE.clear()

    path = common._create_l_trade_order(
        product="EURUSD",
        direction="LONG",
        strategy_key="breakout_demo",
        trade_id="trade-3",
        current_price=1.1,
        mode="net",
        source_group="breakout",
        is_auto_promote=True,
    )

    assert path is None
    assert "max_trades_to_tws reached" in (common._LAST_L_TRADE_ORDER_ERROR or "")


def test_standard_live_order_still_respects_daily_target(tmp_path, monkeypatch):
    monkeypatch.setattr(
        common,
        "_load_config",
        lambda: {
            "archive": False,
            "run_mode": "LIVE",
            "daily_target": 100.0,
            "max_live_trades": 3,
            "max_trades_to_tws": 3,
            "send_json_files": str(tmp_path),
        },
    )
    monkeypatch.setattr(common, "_get_total_open_live_trades_for_group", lambda *_: 0)
    monkeypatch.setattr(common, "_get_group_closed_live_pnl", lambda *_: 250.0)
    monkeypatch.setattr(common, "_get_total_open_tws_sent_trades", lambda *_: 0)
    monkeypatch.setattr(common, "_get_tws_contract_details", _stub_contract)
    monkeypatch.setattr(common, "_trade_quantity_for_product", lambda *_: 1000)
    monkeypatch.setattr(common, "_resolve_product_type", lambda *_: "forex")
    monkeypatch.setattr(common, "_increment_global_active", lambda *_: None)
    common._LIVE_ORDERS_SENT_MEMORY_CACHE.clear()

    path = common._create_l_trade_order(
        product="EURUSD",
        direction="LONG",
        strategy_key="breakout_demo",
        trade_id="trade-4",
        current_price=1.1,
        mode="net",
        source_group="breakout",
    )

    assert path is None
    assert "daily_target reached" in (common._LAST_L_TRADE_ORDER_ERROR or "")


def test_handle_live_orders_auto_promotes_only_when_weekly_net_positive(monkeypatch):
    strategy = _build_strategy_for_auto_promote(monkeypatch)
    create_calls = []

    monkeypatch.setattr(common, "_get_weekly_summary_net", lambda *_: 42.0)

    def _fake_create(self, current_time, current_price, direction, trade_id, mode="net", is_close=False, is_auto_promote=False):
        create_calls.append(
            {
                "mode": mode,
                "direction": direction,
                "trade_id": trade_id,
                "is_close": is_close,
                "is_auto_promote": is_auto_promote,
            }
        )
        return str(FS_DIR / "_auto_promote_test_order.json")

    monkeypatch.setattr(common.BaseBreakoutStrategy, "_create_tradeable_json", _fake_create)

    strategy._handle_live_orders(datetime(2026, 4, 10, 9, 30, 0), 1.1, "LONG")

    assert create_calls == [
        {
            "mode": "net",
            "direction": "LONG",
            "trade_id": "trade-123",
            "is_close": False,
            "is_auto_promote": True,
        }
    ]
    assert strategy.open_trade["order_sent_net"] is True
    assert strategy.open_trade["is_live_trade"] is True


def test_handle_live_orders_blocks_auto_promote_when_weekly_net_not_positive(monkeypatch):
    strategy = _build_strategy_for_auto_promote(monkeypatch)
    create_calls = []

    monkeypatch.setattr(common, "_get_weekly_summary_net", lambda *_: 0.0)
    monkeypatch.setattr(
        common.BaseBreakoutStrategy,
        "_create_tradeable_json",
        lambda self, *args, **kwargs: create_calls.append({"args": args, "kwargs": kwargs}),
    )

    strategy._handle_live_orders(datetime(2026, 4, 10, 9, 30, 0), 1.1, "LONG")

    assert create_calls == []
    assert strategy.open_trade.get("order_sent_net") is None
    assert strategy.open_trade.get("is_live_trade") is None
