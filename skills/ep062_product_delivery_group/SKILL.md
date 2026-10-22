---
name: ep062-product-delivery-group
description: Use when delivering EP062 Strategy Directory evidence.
version: 1.0.0
author: E, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [EP062, Strategy Directory, Interactive HTML, Evidence]
    related_skills: []
---

# EP062 Product Delivery Group

Build a video-ready, interactive HTML evidence explorer from frozen Strategy Directory, Forex Leaderboard and Equity Curves records. Deliver a single self-contained HTML file that explains the selection flow without querying live data, offering trading instructions, or implying future performance.

## When to Use

- Creating or refreshing the EP062 Strategy Directory interactive product.
- Turning a video walkthrough into a static, reviewable evidence companion.
- Adding strategy drill-down, snapshot-selection or equity-curve detail to the explorer.
- Do not use for live dashboards, execution controls, account access, advice, signals, or performance forecasts.

## Prerequisites

- Obtain the exact frozen source exports before editing:
  1. Strategy Directory summary and strategy drill-down response.
  2. Forex Leaderboard snapshot file and timestamp.
  3. Equity Curves response for the selected candidate and date.
- Preserve each source identifier, filter state and evidence date inside the output.
- Treat the strategy Directory Top 1 and a later Forex snapshot candidate as separate records unless the sources prove they are the same strategy.

## Deliverable Contract

- Produce one self-contained `.html` file: no `fetch()`, remote scripts, credentials or hidden dependencies.
- Keep the three-stage narrative:
  1. **Directory** — universe, Top 1 card and drill-down ledger.
  2. **Snapshot selection** — product/scenario comparison and displayed candidate.
  3. **Equity management** — historical curve replay, component splits, competitor cohort and hourly checkpoints.
- Use static source data only; label the snapshot date and source record.
- Use the TheTechPrinciple dark ink / cyan / lime visual language.
- Support 375px mobile without horizontal page overflow and keep touch targets at least 44px high.

## Procedure

1. **Freeze and validate inputs.**
   - Save the Directory, snapshot and Equity Curves responses before building.
   - Completion: identifiers, filter values, dates and record counts are known and can be rendered verbatim.

2. **Build Directory context and drill-down.**
   - Show Directory aggregate context and the exact Top 1 identifier/strategy name for that Directory scope.
   - Embed the complete closed-trade ledger for the selected Directory strategy: trade number, product, side, entry/exit time, entry/exit price, net and alternative net.
   - Provide all/BUY/SELL/positive/negative filters, pagination and a row-detail panel.
   - Completion: every embedded trade count equals the frozen drill-down count; no trade is invented or omitted.

3. **Build the snapshot-selection stage.**
   - Show the frozen snapshot timestamp, product comparison, selected scenario and displayed candidate.
   - State whether the source proves a complete intra-scenario ranking. If not, call it a displayed candidate.
   - Completion: displayed product, scenario, score and candidate match the archived snapshot exactly.

4. **Build the Equity Curves stage.**
   - Embed fixed checkpoints from the selected candidate’s curve and provide Net, BUY and SELL display toggles.
   - Show similar-strategy comparison records from the same frozen cohort.
   - Include hourly checkpoints using completed records only. Mark incomplete/live periods as provisional if they are present.
   - Describe a target only as a historical analytical/replay overlay marker, never as a target to achieve.
   - Completion: component values, comparison rows and time checkpoints match the frozen Equity Curves response.

5. **Apply safety and editorial boundaries.**
   - State that the artifact is historical/analytical only.
   - Exclude live prices, account data, credentials, order controls, recommendations, forecasts, guarantees and managed-trading language.
   - Completion: no control or copy can be read as a live trading instruction.

6. **Verify the artifact.**
   - Use `terminal` to run a static content test that asserts all source identifiers, expected controls and absence of `fetch(`.
   - Use `browser_exec` at desktop and 375px widths to test stage navigation, component toggles, filters, pagination and row details.
   - Completion: test passes; desktop and 375px have no horizontal page overflow; all interactions update from embedded source data.

## Data Rules

- A source snapshot is evidence for its recorded point in time, not a forecast.
- Preserve negative outcomes, drawdown and alternative-net fields; do not curate only favourable rows.
- Keep source scopes separate: an all-history Directory leader is not automatically a leading candidate in a later Forex product snapshot.
- When comparing similar strategies, identify the cohort and source response used.
- Never fabricate hourly totals, trade values, ranks, dates or target-hit statements.

## Pitfalls

- Do not replace a complete drill-down ledger with a hand-picked sample when the product promises detailed trades.
- Do not expose raw GUIDs where sequential trade numbers communicate the detail needed for the explainer.
- Do not load data at browser runtime: the artifact must remain viewable off-platform as a frozen record.
- Do not call historical performance “active management”; call it analysis, replay or recorded overlay logic.
- Do not imply that a target overlay will be achieved in the future.

## Verification Checklist

- [ ] Single HTML file contains all required static data and no runtime network calls.
- [ ] Directory Top 1 card is scoped and source-dated.
- [ ] Full selected-strategy trade ledger is embedded, filterable, paginated and inspectable.
- [ ] Forex snapshot selection chain and source timestamp are visible.
- [ ] Equity stage includes Net/BUY/SELL toggles, competitor cohort and hourly checkpoints.
- [ ] Negative outcomes, drawdown and limitations are retained.
- [ ] Historical/no-advice/no-execution boundary is visible.
- [ ] Automated static test passes.
- [ ] Browser verification passes at desktop and 375px mobile.

## Related skill

For the simplified "Select. Compare. Switch." app that is rebuilt on demand from live PostgreSQL data (single self-contained file), use `ep062-switch-explorer-rebuild/SKILL.md` in this folder. This skill covers the older frozen evidence explorer.
