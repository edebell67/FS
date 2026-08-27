# WF-302 UI/API Reconciliation

| UI value | Fixture/API field | Result |
|---|---|---|
| DNA_102001 | strategy_id | Match |
| 148 trades | total_trades | Match |
| +£6,240 | total_net_return + GBP basis | Match |
| −£810 | max_drawdown_money | Match |
| 54.1% | win_rate | Match |
| 1.72 | profit_factor | Match |
| open EUR/USD BUY +£18 | protected open-state fixture | Match; excluded from history |

PASS — target-reached copy explicitly states that outcome comes from net return; open/unrealized state is isolated from historical metrics.

