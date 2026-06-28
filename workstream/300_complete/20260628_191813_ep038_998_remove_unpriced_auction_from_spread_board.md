# EP038 — Remove Unpriced Auction From Spread Board

Source: User correction: a spread only exists when sale price or guide sale price is known; if sale price is unknown, we are not interested in it as a spread.
Task Type: standard

Task Attributes:
- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: true
- workflow_name: "workstream-task-lifecycle"
- workflow_stage: in_progress
- depends_on:
  - /mnt/c/Users/edebe/eds/epics/ep_038_arbitrage/data/live_spread_board.csv
- feeds_into:
  - EP038 live spread data quality rules

Task Summary: Correct EP038 data model so auction products without known sale/reference/guide price are not included in live spread board metrics/cards.

Context:
- `namedigital.com` has auction-side current cost captured, but no confirmed sale/reference price.
- User clarified that this must not be represented as a spread.

Destination Folder: /mnt/c/Users/edebe/eds/epics/ep_038_arbitrage/

Dependency: Existing live auction proof files.

Plan:
- [x] 1. Remove `SPRD-LIVE-001` from `data/live_spread_board.csv` and `site_launch/data/spreads.json`.
  - [x] Test: Search files and confirm no `SPRD-LIVE-001` in spread board or launch JSON.
  - Evidence: Removed 1 board record; `live_spread_board.csv` and `site_launch/data/spreads.json` now contain 10 sample/demo records and no `SPRD-LIVE-001`.
- [x] 2. Preserve `namedigital.com` only as an auction-watch candidate/observation, not a spread.
  - [x] Test: `data/live_auction_observations.csv` still contains the observation with `sought_not_quantified`.
  - Evidence: `live_auction_observations.csv` still contains `namedigital.com` and `sought_not_quantified`.
- [x] 3. Add documented rule that sale/reference/guide price is mandatory for spread inclusion.
  - [x] Test: Rule file exists and includes required gate.
  - Evidence: Created `EP038_SPREAD_INCLUSION_RULES.md`; patched repeatability skills with spread inclusion gate.
- [x] 4. Regenerate/validate launch data/site metrics.
  - [x] Test: Launch JSON active count returns to sample-only count and HTTP live board loads.
  - Evidence: Launch JSON metrics: active_count=8, total_count=10, auction_watch_count=1, qualified_live_auction_spread_count=0; `live-spreads.html` returned HTTP 200.

Evidence:
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: file_output
  - Artifact: /mnt/c/Users/edebe/eds/epics/ep_038_arbitrage/EP038_SPREAD_INCLUSION_RULES.md
  - Objective-Proved: Spread inclusion gate is documented.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: Validation output: removed_from_board=1, board_records=10, launch_json_records=10, auction_watch_preserved=true, HTTP 200.
  - Objective-Proved: Unpriced auction removed from spread board and preserved as watch candidate.
  - Status: captured

Implementation Log:
- 2026-06-28T19:19:51: Removed unpriced auction from spread board, preserved it as watch-only, documented mandatory sale/reference price inclusion gate.
- 2026-06-28T19:18:13: Task created after user corrected inclusion rule.

Changes Made:
- Removed `SPRD-LIVE-001` from `data/live_spread_board.csv`.
- Removed `SPRD-LIVE-001` from `site_launch/data/spreads.json`.
- Updated `site_launch/index.html` to call `namedigital.com` an auction watch candidate, not a spread.
- Created `EP038_SPREAD_INCLUSION_RULES.md`.
- Updated `spikes/004-live-auction-proof/README.md` with correction note.
- Updated `ARTIFACT_MANIFEST.md`.
- Patched local repeatability skill and Hermes marketplace-arbitrage skill with the inclusion gate.

Validation:
- Confirmed `SPRD-LIVE-001` absent from board CSV and launch JSON.
- Confirmed `namedigital.com` remains in `data/live_auction_observations.csv` with `sought_not_quantified`.
- Confirmed launch JSON metrics include `auction_watch_count=1` and `qualified_live_auction_spread_count=0`.
- Served launch site locally and fetched `live-spreads.html` with HTTP 200.

Risks/Notes:
- Auction-watch records can exist before spread qualification, but must not be counted/published as spreads.

Completion Status: Complete
Completion Date: 2026-06-28T19:19:51
