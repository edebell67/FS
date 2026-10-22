"""Version 1.1.0 (2026-08-28): Updated for the single-query local_strategy_summary()
(strategy_name/product now come from combined_trades_closed directly, not a
separate product_forex round trip - see repository.py 1.8.0).
Version 1.0.0 (2026-08-28): Guard exact-strategy SQL predicate and parameter order."""
from app import repository


def test_exact_strategy_restricts_trade_source_before_aggregation(monkeypatch):
    class Cursor:
        description = []
        calls = 0

        def execute(self, query, *params):
            self.calls += 1
            assert 'GROUP BY' not in query
            assert 'product_forex' not in query
            assert 'model_ix IN (CONVERT(varchar(200),?)' in query
            assert params == ('DNA_201778', 'DNA_201778_B', 'DNA_201778_S', 'start', 'end', 'BUY')

        def fetchall(self):
            return [(10, 'start', 'end', 'example', 'GBP'), (-5, 'start', 'end', 'example', 'GBP'), (0, 'start', 'end', 'example', 'GBP')]

    class Connection:
        def cursor(self):
            return Cursor()

        def close(self):
            pass

    monkeypatch.setattr(repository, 'sqlserver_connection', lambda _: Connection())
    row = repository.local_strategies(None, 'start', 'end', 'DNA_201778', 'BUY')[0]
    assert row['total_trades'] == 3
    assert row['total_net_return'] == 5
    assert row['profit_factor'] == 2
    assert row['breakevens'] == 1
    assert row['descriptive_name'] == 'example'
    assert row['product_name'] == 'GBP'
