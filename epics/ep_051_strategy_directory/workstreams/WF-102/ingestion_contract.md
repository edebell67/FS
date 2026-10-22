# WF-102 Canonical Ingestion Contract

## Source roles

- `combined_trades_closed`: completed trades only; canonical historical analytics source; idempotency key `guid`.
- `combined_trades_open`: current/open state only; never included in closed-trade headline or period analytics.

## Normalization

- Model identifiers are trimmed, uppercased, and terminal `_S`/`_B` is removed for canonical identity.
- The original model value remains in `source_model` for lineage.
- Timestamps are converted to timezone-aware UTC values.
- Exit time is `g_close_time` when present, otherwise `last_update`.
- Numeric results use fixed decimal representation; `net_return` already includes costs.
- Outcome is derived only from `net_return`: positive `winner`, negative `loser`, zero `breakeven`.

## Incremental and replay behavior

- Each source has an independent `(timestamp, stable_id)` watermark.
- Closed records upsert by `guid`; exact replay is a no-op and conflicting replay is quarantined.
- Open records upsert by `guid` and may update the current snapshot without entering closed analytics.
- Invalid records are stored with source, stable identifier, reason, raw payload, run ID, and replay state.
- A run manifest records source watermarks, counts, checksums, duration, status, and failure reason.

