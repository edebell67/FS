## Task

- Modify `C:\Users\edebe\eds\epics\ep_016_turning_point_pattern_engine\logic\price_frequency_gbp_analyzer.py`
- Keep only one open position per product at a time
- If an open buy is already in place, do not open another buy until the previous buy is closed

## Task Type

- implementation

## Project

- ep016

## Destination Folder

- `workstream/300_complete/general`

## Dependency

- Target analyzer: [price_frequency_gbp_analyzer.py](<C:/Users/edebe/eds/epics/ep_016_turning_point_pattern_engine/logic/price_frequency_gbp_analyzer.py>)
- Existing marker/event flow for `<>`, `><`, `<<>>`, `>><<`

## Plan

1. Identify the signal-recording point where open/close markers become persistent events.
2. Add per-product active-position state.
3. Block new open events while a position is already active for that product.
4. Allow only the matching close event to release the product for a future open.

## Evidence

- Added `active_position_by_symbol` to track the currently open position direction per product.
- Added `marker_position_direction()` to normalize marker states into `long` / `short`.
- Added `should_record_trade_event()` to enforce:
- first open is accepted only when no active position exists
- duplicate opens are rejected while a position is active
- wrong-direction closes are rejected
- only the matching close clears the active position
- Updated the analyzer loop so marker detection can still occur, but only permitted trade events are actually recorded into marker history and the right-side trade-event panel.

## Validation

- `python -m py_compile epics/ep_016_turning_point_pattern_engine/logic/price_frequency_gbp_analyzer.py`
- Deterministic gate validation:
- `open_long_1 -> True, active=long`
- `open_long_2 -> False, active=long`
- `close_short_wrong -> False, active=long`
- `close_long -> True, active=None`
- `open_short -> True, active=short`
- `close_short -> True, active=None`

## Completion Status

- Complete
