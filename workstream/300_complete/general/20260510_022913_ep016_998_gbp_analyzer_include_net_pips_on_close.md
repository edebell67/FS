## Task

- Modify `C:\Users\edebe\eds\epics\ep_016_turning_point_pattern_engine\logic\price_frequency_gbp_analyzer.py`
- Include net pip return on close events

## Task Type

- implementation

## Project

- ep016

## Destination Folder

- `workstream/300_complete/general`

## Dependency

- Target analyzer: [price_frequency_gbp_analyzer.py](<C:/Users/edebe/eds/epics/ep_016_turning_point_pattern_engine/logic/price_frequency_gbp_analyzer.py>)
- Existing trade event log: [price_frequency_gbp_analyzer_trade_signals.txt](<C:/Users/edebe/eds/epics/ep_016_turning_point_pattern_engine/logic/price_frequency_gbp_analyzer_trade_signals.txt>)
- Existing single-open-position state

## Plan

1. Extend active position state to keep entry price and entry timestamp.
2. On close, compute pip return from stored entry price and the close trigger price.
3. Append the calculated pip return to the close event payload and `.txt` log output.
4. Validate with a deterministic trade example.

## Evidence

- Added `infer_pip_multiplier()` with JPY-aware pip scaling.
- Added `compute_net_pips()` to calculate pip return for long and short closes.
- Expanded `active_position_by_symbol` from a simple direction flag into a full entry record including:
- direction
- entry price
- entry timestamp
- entry bucket
- entry state
- entry side
- Updated close-event gating so the accepted close event is enriched with:
- `entry_price`
- `entry_timestamp`
- `net_pips`
- Updated the text log writer so close events append `entry_price` and `net_pips`.

## Validation

- `python -m py_compile epics/ep_016_turning_point_pattern_engine/logic/price_frequency_gbp_analyzer.py`
- Deterministic long-trade validation:
- open at `1.3003`
- close at `1.3011`
- computed `net_pips = 8.0`
- Logged close line:
- `2026-05-10 10:10:31 | symbol=GBP | side=ASK | event=CLOSE | bucket=10:10 | price=1.3011 | count=23 | marker=>23< | state=EXIT_LONG_CANDIDATE_HIGH | entry_price=1.3003 | net_pips=8.0`

## Completion Status

- Complete
