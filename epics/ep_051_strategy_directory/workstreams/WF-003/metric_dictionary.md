# Metric Dictionary - EP051 DNA Strategy Directory

## Core Formulas
Let closed trade returns be `r_i = net_return_i`, ordered by validated exit time.

- `total_trades`: `count(valid closed trades)`
- `wins`: `count(r_i > 0)`
- `losses`: `count(r_i < 0)`
- `breakevens`: `count(r_i == 0)`
- `win_rate`: `wins / total_trades`
- `total_net_return`: `sum(r_i)`
- `average_trade`: `mean(r_i)`
- `median_trade`: `median(r_i)`
- `gross_profit`: `sum(r_i where r_i > 0)`
- `gross_loss`: `abs(sum(r_i where r_i < 0))`
- `profit_factor`: `gross_profit / gross_loss` (null if gross_loss is 0)
- `average_win`: `mean(r_i where r_i > 0)`
- `average_loss`: `mean(r_i where r_i < 0)`
- `payoff_ratio`: `average_win / abs(average_loss)`
- `expectancy`: `(win_rate * average_win) + (loss_rate * average_loss)`
- `holding_minutes`: `exit_time - created`
- `trades_per_day`: `total_trades / documented_active_day_denominator`

## Drawdown (Monetary Only Unless Equity Provided)
- `E_t`: `cumulative_sum(r_i)`
- `peak_t`: `max(E_0 ... E_t)`
- `drawdown_t`: `E_t - peak_t`
- `max_drawdown`: `min(drawdown_t)`

## Edge Cases
- **Zero Denominators**: Profit factor and payoff ratio must return `null` if the denominator is 0. Do not convert to infinite or 0.
- **Missing Values**: Missing values are preserved as null, not zero.
- **Percentages**: Never label currency P&L aggregate as a percentage. Drawdown percentage requires explicitly defined capital/equity basis.

## Windows and Timezones
- **Timezone**: All analytics are aggregated using UTC.
- **Calendar**: Trading days exclude weekends and recognized market holidays (e.g. standard FX market closure hours).
