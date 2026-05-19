# Deploy Backtest-to-Live Parity Audit Kit public pages

## Task Type
Deployment / static hosting

## Destination
GitHub Pages via edebell67/epics master branch, /backtest-live-parity-audit-kit/ path.

## Dependency
Parent kanban task t_20b21c7c produced v0.2 product package and public pages.

## Plan
- Copy public landing/download/intake HTML into a tracked GitHub Pages directory.
- Copy the v0.2 ZIP alongside the pages.
- Adjust download links to use same-directory ZIP URL.
- Push only the deployment files and this lifecycle note.
- Verify public URLs with HTTP checks after push.

## Evidence
- Commit pushed: 6b5d47ee (`Deploy parity audit kit landing pages`).
- Public landing URL: https://edebell67.github.io/epics/backtest-live-parity-audit-kit/
- Public download URL: https://edebell67.github.io/epics/backtest-live-parity-audit-kit/download.html
- Public intake URL: https://edebell67.github.io/epics/backtest-live-parity-audit-kit/audit-intake.html
- Public ZIP URL: https://edebell67.github.io/epics/backtest-live-parity-audit-kit/backtest_live_parity_audit_kit_v0_2.zip

## Implementation Log
- 2026-05-18 21:16: Began deployment task.
- 2026-05-18 21:18: Created tracked GitHub Pages directory `backtest-live-parity-audit-kit/`, copied three HTML pages and v0.2 ZIP, adjusted ZIP hrefs to same-directory paths, and replaced unresolved Stripe placeholders with explicit pending anchors.
- 2026-05-18 21:19: Committed and pushed deployment files to `origin/master`.
- 2026-05-18 21:20: Verified all public URLs return HTTP 200.

## Changes
- Added `backtest-live-parity-audit-kit/index.html`.
- Added `backtest-live-parity-audit-kit/download.html`.
- Added `backtest-live-parity-audit-kit/audit-intake.html`.
- Added `backtest-live-parity-audit-kit/backtest_live_parity_audit_kit_v0_2.zip`.

## Validation
- HTTP 200 verified for landing, download, intake, and ZIP URLs.
- Downloaded public ZIP SHA-256 matched local deployed ZIP: `1b5141aefcc7618573034c74f65ed33616878c05fb4ed470316b536577919131`.
- Python `zipfile.testzip()` returned ok for the downloaded public ZIP.
- Page titles verified for all three public HTML pages.

## Risks
Stripe payment links are not available yet, so landing checkout buttons are non-checkout pending anchors until Ed creates the links. Stripe success URLs can now be configured to the public download/intake URLs above.

## Completion Status
Complete.
