# Regime Specification - EP051 DNA Strategy Directory

## 1. Objective Rules
Regime tagging applies to canonical market contexts to slice strategy performance.
Rules rely strictly on objective market features computed globally, not individually derived from DNA strategy performance.

### 1.1 Directional Regime
Computed using a 20-day Simple Moving Average (SMA) vs 50-day SMA of the underlying instrument's daily closing price.
- **Bullish**: `SMA_20 > SMA_50 + 0.5%`
- **Bearish**: `SMA_20 < SMA_50 - 0.5%`
- **Neutral (Ranging)**: `abs(SMA_20 - SMA_50) <= 0.5%`

### 1.2 Volatility Regime
Computed using the 14-day Average True Range (ATR) normalized as a percentage of the 14-day closing price average (NATR).
- **High Volatility**: `NATR > 80th percentile (of trailing 252 days)`
- **Low Volatility**: `NATR < 20th percentile (of trailing 252 days)`
- **Normal Volatility**: `20th <= NATR <= 80th percentile`

### 1.3 `UNKNOWN` Fallback
If historical price data is missing or lookback windows (e.g. 50 days) are not fully satisfied, the regime defaults to `UNKNOWN`.

## 2. Anti-Bias Protocol
- **No Future Data**: Regime state for trade `t` at time `T` must only use market data available at `T - 1 day` (i.e., yesterday's close). 
- **Independence**: Regime state calculation cannot use strategy equity curves, DNA identifiers, or trade P&L in its inputs.
- **Version Freeze**: The threshold parameters (0.5% threshold, 20/80 percentiles) are frozen in this version (v1.0.0) before observing any strategy's cross-regime performance to prevent p-hacking.
