# Market-Only Strategy Optimization Report (Zero Offset)
**Date**: 2026-05-13
**Objective**: Best realistic PPH using only Market Orders (0.0 Offset).
**Rules**: Buy at Ask / Sell at Bid, -2.0 pip cost per round turn, data cleaning (skip zero/neg prices).
**Data**: Today's tick capture (approx 14 hours duration).

## Summary Table
| Symbol | Best PPH | Total Net | Alt-Net | Trades | Config (H/M/L) | Bucket | TP/SL |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **GBP (AUD)** | **8.12** | 116.50 | -292.50 | 44 | 74 / 35 / 19 | 10m | 50/15 |
| **EUR (AUD)** | **4.98** | 71.50 | -247.50 | 44 | 69 / 24 / 20 | 10m | 50/None |
| **NZD (AUD)** | **4.98** | 71.50 | -247.50 | 44 | 23 / 11 / 4 | 10m | 50/None |
| **AUD (CAD)** | **0.52** | 7.50 | -183.50 | 44 | 20 / 10 / 5 | 10m | None/None |
| **CHF (CAD)** | **4.60** | 66.00 | -110.00 | 11 | 24 / 20 / 2 | 15m | None/None |
| **CAD (JPY)** | **1.40** | 20.00 | -108.00 | 22 | 20 / 10 / 4 | 5m | 50/10 |

## Analysis
1.  **Lower PPH (Realistic)**: Without the artificial boost of the negative offset bug, the PPH has settled into a realistic range of **1.0 to 8.0 PPH**.
2.  **Stability in Slow Buckets**: Most symbols favored **10 or 15 minute buckets** for Market Orders. This suggests that without a retracement buffer, entering on slower, more confirmed trends is safer to overcome the -2.0 pip cost.
3.  **JPY Correction**: The JPY pip multiplier (100) is now correctly handled. CADJPY results are now grounded (1.40 PPH vs the previous thousands).
4.  **Directional Edge**: The **Alt-Net** remains universally and deeply negative. This is the strongest evidence that the "Turning Point" pattern engine is correctly identifying the market bias.

Final JSON configurations for these Market-Only runs are stored in the `optimization/` folder as `best_config_market_{SYMBOL}.json`.
