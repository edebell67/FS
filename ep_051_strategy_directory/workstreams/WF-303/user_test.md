# WF-303 User Test — Compare, Watchlist, and Explanation

## Version history

- 1.0.0 (2026-08-23): Initial verified user test.

## Result

PASS.

## Scenarios

1. Open `compare.html`; confirm DNA_102001 and DNA_102002 render side by side with a compatible GBP, 1Y evidence basis.
2. Open the Net Return evidence drawer; confirm source, window, sample count, methodology version, quality and limitations are visible and keyboard focus moves into the drawer.
3. Select DNA_102004 as the second strategy; confirm the comparison is blocked because market, currency basis and window are incompatible.
4. Save both strategies; confirm the watchlist stores canonical DNA IDs only and remains available after reload.
5. Copy/share the comparison; confirm the URL contains only strategy IDs and evidence window, with no open-position or private account data.
6. Resize to 390 × 844; confirm controls, evidence table and explanatory content remain usable without hidden actions.

## Evidence

- `screenshots/evidence-drawer.png`
- `screenshots/incompatible-watchlist.png`
- `screenshots/mobile-compare.png`

