Source: User request to review the impact of changing `TradeApps/breakout/fs/json/live` to `TradeApps/breakout/fs/json/{product_type}/live`.

Context:
- `C:\Users\edebe\eds\TradeApps\breakout\fs`

Plan:
- [x] 1. Trace direct and indirect `json/live` assumptions in FS runtime, API, workflows, UI, and utilities.
  - [x] Test: Search for `json/live` and `json/<run_mode>` path construction patterns.
  - [x] Evidence: Confirmed hard-coded `json/live` usages in analysis/helpers and pervasive runtime path composition as `json / run_mode / date`.
- [x] 2. Summarize the architectural impact and primary breakpoints.
  - [x] Test: Prepare review findings with concrete file references.
  - [x] Evidence: Findings prepared for user response.
