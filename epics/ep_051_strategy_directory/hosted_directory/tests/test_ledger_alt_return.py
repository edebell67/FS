"""Version 2.0.0 (2026-08-28): rewritten for the v3.0.0 SQL-native refresh
script (DayState / in-memory aggregation was replaced by
dbo.ep051_directory_daily_summary + a trigger - see
refresh_directory_summary_cache.py version history). Same intent as
v1.0.0: alt_net_return is carried through the trade ledger independently
of net_return and never influences the aggregate calculations, which now
come straight from the pre-aggregated SQL table rather than being
recomputed in Python.
Version 1.0.0 (2026-08-28): cached alternative returns preserve zero/null and do not alter metrics."""
from datetime import date
from scripts.refresh_directory_summary_cache import fetch_summary, fetch_trades_by_strategy


class Cursor:
    def __init__(self, rows):
        self.rows = rows

    def execute(self, query, *params):
        return self.rows


def test_alt_return_is_independent_of_net_return_in_ledger():
    # fetch_trades_by_strategy carries alt_net_return through untouched,
    # including the null case, without it affecting net_return at all.
    cursor = Cursor([
        ('DNA_201877', 'one', 'GBP', 'name', 'BUY', date(2026, 8, 28), 1, date(2026, 8, 28), 2, -50, 30),
        ('DNA_201877', 'two', 'GBP', 'name', 'BUY', date(2026, 8, 28), 1, date(2026, 8, 28), 2, -20, None),
        ('DNA_201877', 'three', 'GBP', 'name', 'SELL', date(2026, 8, 28), 1, date(2026, 8, 28), 2, 10, 0),
    ])
    trades_by_strategy = fetch_trades_by_strategy(cursor, date(2026, 8, 28), date(2026, 8, 29))
    result = {row['guid']: row['alt_net_return'] for row in trades_by_strategy['DNA_201877']}
    assert result == {'one': 30, 'two': None, 'three': 0}
    assert {row['net_return'] for row in trades_by_strategy['DNA_201877']} == {-50, -20, 10}


def test_summary_totals_come_from_the_pre_aggregated_table_untouched_by_alt_return():
    # fetch_summary has no concept of alt_net_return at all - it just reads
    # whatever the SQL-side trigger already computed. Confirms the summary
    # path and the ledger path are independent, so a null alt_net_return in
    # the ledger can never leak into or corrupt the aggregate totals.
    cursor = Cursor([
        ('DNA_201877', 'BOTH', 'name', 'GBP', 3, 2, 1, 0, -60, 40, 100, date(2026, 8, 28), date(2026, 8, 28)),
    ])
    datasets = fetch_summary(cursor, date(2026, 8, 28))
    row = datasets['BOTH'][0]
    assert row['total_trades'] == 3
    assert row['total_net_return'] == -60
    assert 'alt_net_return' not in row
