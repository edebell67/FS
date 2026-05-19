## Task

- Modify `C:\Users\edebe\eds\epics\ep_016_turning_point_pattern_engine\logic\price_frequency_gbp_analyzer.py`
- Output the open and close trade details signalled by `<>` and `><`, including timestamp
- Display those trade events in a window/panel viewable on the right-hand side of the screen

## Task Type

- implementation

## Project

- ep016

## Destination Folder

- `workstream/100_backlog/general`

## Dependency

- Target analyzer: [price_frequency_gbp_analyzer.py](<C:/Users/edebe/eds/epics/ep_016_turning_point_pattern_engine/logic/price_frequency_gbp_analyzer.py>)
- Existing trade marker logic:
- open markers: `<>`, `<<>>`
- close markers: `><`, `>><<`
- Existing console rendering and snapshot table layout

## Plan

1. Review the current trade-marker generation path and identify the exact event data available at open/close signal time.
2. Define a trade-event record shape that captures at least timestamp, symbol, side, event type, bucket, price row, and displayed frequency value.
3. Add an on-screen right-side panel/window that lists recent open/close signal events without removing the existing in-table markers.
4. Validate that new `<>` and `><` events appear in the right-side view with timestamps and remain readable alongside the main snapshot table.

## Evidence

- Task opened to add a dedicated right-side trade-event view for `<>` / `><` marker signals.
- User requirement is to show open/close trade details with timestamp in a viewable right-hand-side window while preserving existing marker behavior.
- Updated [price_frequency_gbp_analyzer.py](<C:/Users/edebe/eds/epics/ep_016_turning_point_pattern_engine/logic/price_frequency_gbp_analyzer.py>) to capture each recorded marker event into a `recent_trade_events` list.
- Each recorded event now includes:
- source timestamp
- symbol
- side (`ASK` / `BID`)
- event type (`OPEN` / `CLOSE`)
- snapshot bucket
- price row
- signed frequency count
- rendered marker form such as `<<54>>`, `>>-23<<`, `<<-7>>`
- Reworked the console renderer to build a left snapshot panel and a right trade-signal panel, then print them side by side.
- The right-side panel now shows recent `<>` / `><` events in reverse chronological order while the main table keeps the historical markers in place.

## Validation

- `python -m py_compile epics/ep_016_turning_point_pattern_engine/logic/price_frequency_gbp_analyzer.py`
- Synthetic side-by-side render validation confirmed the right-side panel displays timestamped events such as:
- `2026-05-10 10:00:05 GBP`
- `OPEN BID <<-7>> @ 1.2998`
- `bucket=10:00 state=SHORT_ENTRY_CANDIDATE_LOW`
- `2026-05-10 10:10:31 GBP`
- `CLOSE ASK >>-23<< @ 1.3001`
- `bucket=10:10 state=EXIT_LONG_CANDIDATE_HIGH`
- Main snapshot table remained visible on the left with historical `<>` / `><` markers preserved.

## Completion Status

- Complete
