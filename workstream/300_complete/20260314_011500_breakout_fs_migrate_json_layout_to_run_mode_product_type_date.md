Source: User request to fully document and proceed with the FS JSON layout migration after impact review.

Context:
- `C:\Users\edebe\eds\TradeApps\breakout\fs`

Goal:
- Migrate the FS JSON storage model from `json/{run_mode}/{date}` to `json/{run_mode}/{product_type}/{date}`.
- Preserve operational continuity by keeping reads backward-compatible where feasible during the transition.

Plan:
- [ ] 1. Trace how `product_type` is derived in the FS runtime and identify the highest-impact write/read paths.
  - [ ] Test: Inspect runtime config, trade data structures, and JSON path helpers.
  - [ ] Evidence: Pending.
- [ ] 2. Implement shared path resolution helpers and update core runtime writers/readers to use the new layout.
  - [ ] Test: Core FS runtime, archive, summary generation, and API day-directory resolution all route through the new layout.
  - [ ] Evidence: Pending.
- [ ] 3. Add backward-compatible read fallbacks for legacy `json/{run_mode}/{date}` data.
  - [ ] Test: Readers can still locate legacy data when product-type subfolders are absent.
  - [ ] Evidence: Pending.
- [ ] 4. Validate affected modules and summarize migration notes, remaining risks, and restart requirements.
  - [ ] Test: Syntax validation plus targeted path-resolution checks.
  - [ ] Evidence: Pending.
