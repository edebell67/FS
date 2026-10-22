# WF-104 Market and Regime Data Contract

## Instrument and calendar identity

Each observation uses canonical `instrument_id`, `market`, timezone, session calendar, quote currency and price precision. FX v1 uses UTC daily buckets and records session-closure policy explicitly.

## Feed and feature rules

- Raw bars are immutable by `(instrument_id, interval, bucket_start, provider_version)`.
- Regime features use only bars whose `available_at` is earlier than the classified interval.
- Direction uses frozen SMA20/SMA50 rules from WF004.
- Volatility uses NATR14 and trailing 252-observation 20th/80th percentiles.
- Insufficient lookback, missing bars, stale data or failed quality checks produce `UNKNOWN`; values are never silently forward-filled.

## Temporal joins

A trade/event at `event_time` joins the latest regime observation satisfying `observation.available_at <= event_time`. Later observations are ineligible even when their market bucket is earlier. Ties are resolved by frozen definition version and then highest source version.

## Quality and lineage

Every regime observation includes feature values, thresholds, definition version, source watermark, `available_at`, quality state and confidence. Coverage reports separate directional, volatility and fully-known coverage.

