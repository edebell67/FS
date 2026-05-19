## Task

- Modify `C:\Users\edebe\eds\epics\ep_016_turning_point_pattern_engine\logic\price_frequency_gbp_analyzer.py`
- Output emitted trade signals to a `.txt` file

## Task Type

- implementation

## Project

- ep016

## Destination Folder

- `workstream/300_complete/general`

## Dependency

- Target analyzer: [price_frequency_gbp_analyzer.py](<C:/Users/edebe/eds/epics/ep_016_turning_point_pattern_engine/logic/price_frequency_gbp_analyzer.py>)
- Existing right-side trade signal panel
- Existing single-open-position gating

## Plan

1. Hook file logging at the same point where trade events are accepted and recorded.
2. Keep the log append-only so the file remains a historical event trail.
3. Include timestamp, symbol, side, event type, bucket, price, signed count, marker text, and state.
4. Validate the file contents with synthetic open/close events.

## Evidence

- Added `TRADE_SIGNAL_LOG_FILE` at [price_frequency_gbp_analyzer_trade_signals.txt](<C:/Users/edebe/eds/epics/ep_016_turning_point_pattern_engine/logic/price_frequency_gbp_analyzer_trade_signals.txt>).
- Added `append_trade_signal_log()` so each accepted trade event is written to the text log at the same time it is added to the in-memory event list.
- Updated `record_trade_marker()` so the logged payload stays aligned with the right-side panel:
- timestamp
- symbol
- side
- `OPEN` / `CLOSE`
- bucket
- price
- signed count
- rendered marker form
- state

## Validation

- `python -m py_compile epics/ep_016_turning_point_pattern_engine/logic/price_frequency_gbp_analyzer.py`
- Synthetic log validation produced:
- `2026-05-10 10:05:12 | symbol=GBP | side=ASK | event=OPEN | bucket=10:05 | price=1.3003 | count=54 | marker=<54> | state=LONG_ENTRY_CANDIDATE_MEDIUM`
- `2026-05-10 10:10:31 | symbol=GBP | side=ASK | event=CLOSE | bucket=10:10 | price=1.3001 | count=-23 | marker=>-23< | state=EXIT_LONG_CANDIDATE_HIGH`

## Completion Status

- Complete
