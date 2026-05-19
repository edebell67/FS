# Workstream Task: Split/Combo Chart Toggle

## Source
Created from user request on 2026-03-10 to add a contextual split/combo toggle pair to the `/fs` multi-chart cards so traders can work with total vs. buy/sell constituents interchangeably. Mirrors must be added for `multi_chart`, `multi_chart_v2`, and `multi_chart_v3`.

## Task Summary
On breakout multi-chart cards, the existing metric controls should be extended with a contextual toggle:

- `s`: visible only when the card displays the total `net` curve (`[T]`), and when clicked replaces that single total-net line with overlapping `buy_net` and `sell_net` lines on the same axis in the same card.
- `c`: visible only when the card already displays both `buy_net` and `sell_net` (`[B]` and `[S]`), and when clicked restores a single `net` line.
- No iconography or visible `"Split Chart"` / `"Combo"` labels are allowed in the final control.
- Implement the same behavior for the active multi-chart variants.

## Context
- `TradeApps\breakout\fs\multi_chart.html` + related `multi_chart*.js` files
- `TradeApps\breakout\fs\multi_chart_v2.html/js` and `multi_chart_v3.html/js`
- Data flow already supports saving/loading multiple cards and reusing metric strings (`net`, `buy_net`, `sell_net`) via the bucket helpers.

## Plan
- [x] 1. Confirm how `multi_chart.js`, `_v2.js`, and `_v3.js` currently render cards when `net`, `buy_net`, or `sell_net` are selected and identify where to inject the toggle controls.
- [x] 2. Design the `s`/`c` actions so they reconfigure the same card between single total-net and overlapping buy/sell lines while preserving existing save/restore flows.
- [x] 3. Implement the toggle wiring across all active chart scripts, ensuring the UI only shows `s` in total-net state and `c` in paired buy/sell state, with no icon.
- [ ] 4. Test the behavior manually: start with a `[T]` card, click `s` to generate overlapping `[B]/[S]`, then click `c` to return to `[T]`, and verify the button keeps alternating correctly.

## Implementation Log
- **2026-03-10 14:30:00**: Task created to add contextual split/combo chart toggles for multi-chart cards. Work will follow the documented lifecycle.
- **2026-03-10 16:10:00**: First implementation added a split/combo state machine, but the UX was rejected because it used icon-based affordances and did not match the requested `s`/`c` control.
- **2026-03-10 16:56:00**: Corrected the active `DB` implementation so the control is text-only (`s` / `c`), only appears in valid total-net or buy/sell-pair states, and keeps the split view as two overlapping line charts on one axis in the same card.

## Changes Made
- `TradeApps\breakout\DB\multi_chart.js`: replaced the split/combo icon with a text-only stateful button, constrained visibility to valid `[T]` and `[B]/[S]` states, and preserved same-axis overlapping line rendering in the split state.
- `TradeApps\breakout\DB\multi_chart_v2.js` and `TradeApps\breakout\DB\multi_chart_v3.js`: mirrored the same `s`/`c` control model and matching state/visibility logic.
- `TradeApps\breakout\DB\multi_chart.html`, `multi_chart_v2.html`, and `multi_chart_v3.html`: updated styling so the toggle renders as a small text control rather than an icon button.

## Validation
- Pending manual verification after refreshing the active `DB` UI: on `multi_chart.html`, confirm total-net cards show `s`, split them into same-axis `[B]/[S]` lines, then confirm the button flips to `c` and restores single total-net on click.
- Repeat the same cycle on `multi_chart_v2.html` and `multi_chart_v3.html`.

## Risks/Notes
- Replacing cards may interact with the saved bucket logic (which tracks `strategy | product | metric`). Careful coordination is needed to avoid partial saves when splitting/combo occurs mid-session.

## Completion Status
In progress. Awaiting user verification.


# User Feedback
User Verified: PASS
