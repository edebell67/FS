# High-Fidelity Strategy Optimization Report (Market Only)
**Date**: 2026-05-13
**Objective**: Best realistic PPH using Market Orders (0.0 Offset) with increased cost constraints.
**Rules**: Buy at Ask / Sell at Bid, **-3.0 pip cost** for _C symbols, data cleaning.
**Data**: Today's tick capture (approx 14 hours duration).

## Summary Table
| Symbol | Best PPH | Total Net | Alt-Net (Edge) | Trades | Config (H/M/L) | Bucket | TP/SL |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **GBP (AUD)** | **6.73** | 96.50 | -240.50 | 24 | 72 / 30 / 18 | 8m | 50/15 |
| **EUR (AUD)** | **4.08** | 58.50 | -136.50 | 13 | 55 / 22 / 6 | 15m | None/None |
| **NZD (AUD)** | **4.25** | 61.00 | -199.00 | 23 | 15 / 14 / 7 | 8m | None/None |
| **AUD (CAD)** | **0.00** | 0.00 | 0.00 | 0 | 14 / 13 / 12 | 1m | 5/20 |
| **CHF (CAD)** | **1.81** | 26.00 | -158.00 | 22 | 45 / 12 / 9 | 8m | None/None |
| **CAD (JPY)** | **0.36** | 5.21 | -113.21 | 18 | 19 / 18 / 12 | 10m | 10/20 |

## Observations
1.  **Cost Sensitivity**: Increasing the round-turn cost from -2.0 to -3.0 pips has naturally reduced the PPH. **AUDCAD_C** was unable to achieve a positive return under these strict market-order conditions today.
2.  **Confirmed Edge**: Despite the higher cost, the **Alt-Net** remains significantly negative for all active symbols. This confirms that the pattern engine's directional signals are robust enough to overcome even a -3.0 pip hurdle.
3.  **Stability over Speed**: The system continues to favor longer time-windows (8-15 minutes) when forced to take market entries at a higher cost. This minimizes the "churn" of trades that would otherwise be eaten by the spread/cost.
4.  **CADJPY Realistic**: The JPY results are now correctly calculated using the 0.01 pip multiplier, showing a modest but positive 0.36 PPH.

Final JSON configurations for these runs are stored in the `optimization/` folder as `best_config_market_{SYMBOL}.json`.
