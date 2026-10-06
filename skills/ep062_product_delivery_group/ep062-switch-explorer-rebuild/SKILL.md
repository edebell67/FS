---
name: ep062-switch-explorer-rebuild
description: Re-create the EP062 "Select. Compare. Switch." interactive web app on demand with up-to-date data, for crypto and forex (kept separate, chosen with an asset-class switch). Use when asked to rebuild, refresh, update, regenerate, timestamp or send a new version of the strategy selection / compare / switch explorer, or to build it for a different date, product or asset class. Produces ONE self-contained, timestamped html file (data embedded, no server, no network) that users open by double-clicking.
version: 1.1.0
---

# EP062 Switch Explorer: rebuild on demand

> VERSION HISTORY
> - v1.4.0 · 2026-10-05 · History is kept: never delete a previous timestamped build. New `--as-of` option rebuilds how the data stood at a past time (history copies named `...-asof-YYYYMMDD-HHMM.html`).
> - v1.3.1 · 2026-10-05 · Closed-position filter removed (default `--min-closed 0`); page wording follows the stored value; verification checks for stale filter wording (26 checks).
> - v1.3.0 · 2026-10-05 · "Browse the strategy repository" link opens a static, evenly spread sample of the repository (24 per class) as full-day equity curves; verification 25 checks.
> - v1.2.0 · 2026-10-05 · "Always switch" now switches only when the other strategy's net is higher than the one held; default date is the newest day with any data (`--min-hours 1`) so forex and crypto are both current; verification 22 checks.
> - v1.1.0 · 2026-10-05 · Forex added with a Crypto | Forex switch (never pooled); each class has its own date and data-as-of time; output file is timestamped (`...-YYYYMMDD-HHMM.html`) with a `-latest` copy and the build time embedded; compact data encoding (file about 3 MB instead of 8 MB); verification now 21 checks.
> - v1.0.3 · 2026-10-04 · "All products" option (default) pools every loaded product for selection and comparison.
> - v1.0.2 · 2026-10-04 · Mobile first layout rules added; verification now 17 checks.
> - v1.0.1 · 2026-10-04 · Comparison targets must be a different strategy with a different net (no fallback to the selected one); verification now 14 checks.
> - v1.0.0 · 2026-10-04 · First version: rebuild script, verification script, delivery and wording rules.

The explorer is a three-stage page: **1 Strategy selection** (a scenario picks one strategy), **2 Compare** (best similar, best opposite, best overall, best win rate), **3 Switch** (replay what happened after switching, including "always switch, only when better" hour by hour). It shows equity-curve charts of the selected strategies in stages 1 and 2, and the replay in stage 3. An **Asset class** switch at the top (Crypto | Forex) chooses which market is shown. A **Browse the strategy repository** button opens a full-screen sheet with a static sample of the repository as equity-curve cards, so users can see what the selection is made from.

## When to use

- "Rebuild / refresh / update the switch explorer", "send users the latest version", "timestamp it", "build it for forex / for date X / for product Y".
- Do not use for live dashboards, accounts, execution, advice or forecasts. The page is a historical, analytical replay.

## Where things live

| Item | Path (repo root `C:\Users\edebe\eds`) |
|---|---|
| Builder (source of truth) | `epics/ep_062_product_delivery/build_switch_explorer.py` |
| Page template (all HTML, CSS, JS) | `epics/ep_062_product_delivery/switch_explorer_template.html` |
| Output, timestamped | `epics/ep_062_product_delivery/strategy-selection-to-switch-YYYYMMDD-HHMM.html` |
| Output, newest copy | `epics/ep_062_product_delivery/strategy-selection-to-switch-latest.html` |
| Verification | `skills/ep062_product_delivery_group/ep062-switch-explorer-rebuild/scripts/verify_explorer.py` |
| Older frozen evidence explorer (different product) | `epics/ep_062_product_delivery/strategy-directory-evidence-explorer-drilldown.html` |

Edit the template or builder for any change. Never hand-edit the generated html: the next rebuild overwrites it.

## Prerequisites

- Python 3 with `psycopg` installed.
- Read access to PostgreSQL `tradedb`. The builder takes `--dsn`, else env `SOURCE_DATABASE_URL`, else the EP058 settings (`epics/ep_058_strategy_intelligence_pg/hosted_directory/.env`). Never print or quote the connection string or any password.
- **PostgreSQL only, read-only.** Do not touch SQL Server. The builder only runs `select` statements on `tbl_dna_model_summary_snapshots_5min`, `product_forex` and `combined_trades_closed`.

## Rebuild (default: crypto and forex, each on its latest usable day)

```powershell
cd C:\Users\edebe\eds\epics\ep_062_product_delivery
python build_switch_explorer.py
```

The default build takes about 6 minutes (forex has many strategies); run it in the background and wait for the final `wrote ...` and `refreshed ...` lines. A single class is faster: `--product-type crypto` is about 1 minute.

Options:

| Option | Meaning |
|---|---|
| `--product-type both\|crypto\|forex` | Which asset classes to include. Default `both`. |
| `--date YYYY-MM-DD` | Day to replay, applied to every class. Default: each class uses its own newest day with data, so users always get the most recent day (a class can still show an earlier date than the other, for example forex on a weekend). The page shows each class's date. |
| `--min-hours 1` | Hours of snapshots a day needs when picking the default date. Keep 1 so the page is never behind; raise it only if asked to prefer full days. |
| `--products avax,btc` | Comma list of products; only with a single `--product-type`. Default: every product of the class. |
| `--first-hour 3` | Earliest decision hour. |
| `--min-closed 0` | Optional minimum of closed positions a strategy needs to qualify. **Default 0 = no filter.** Never set it unless the user asks; it was removed on request because no such filter was wanted. If used, the value is stored in the file and the page wording follows it. |
| `--as-of ...` | Rebuild as the data stood at a past time, to restore or recreate a history copy: `--as-of "2026-10-05 12:38"` for every class, or `--as-of "crypto=2026-10-05 12:33,forex=2026-10-05 12:38"` per class. Combine with `--date`. Only snapshots and closed positions at or before the cutoff (to the end of that minute) are used. The file is named `strategy-selection-to-switch-asof-YYYYMMDD-HHMM.html` (the newest class cutoff), does not touch `-latest`, and its header says it was rebuilt from stored data. The data-as-of times are the original ones; the "built" time is when the rebuild ran. |
| `--out path.html` | Output file. With `--out` no `-latest` copy is made. |
| `--no-latest` | Do not refresh the `-latest` copy. |
| (automatic) | Inside each class, when two or more products are loaded the page gets an **All products** option (the default), pooling that class only. |

Output naming: without `--out` the builder writes `strategy-selection-to-switch-YYYYMMDD-HHMM.html` (the build time) and refreshes `strategy-selection-to-switch-latest.html`. The build time is also inside the file: a `generated` meta tag, a leading html comment, and the visible header stamp (`Data as of Crypto ... · Forex ... · built ...`).

If a product has no snapshots on the day it is skipped (forex has many `_c`/`_s` products that are often empty). If a whole class has nothing it is left out and the switch hides. If nothing qualifies at all, the builder stops with an error.

For a day still in progress the page uses the latest snapshot and offers every hour that has snapshots. Early hours may be thin; the page says so instead of failing.

## Verify (always, before sending)

```powershell
cd C:\Users\edebe\eds
python skills/ep062_product_delivery_group/ep062-switch-explorer-rebuild/scripts/verify_explorer.py epics/ep_062_product_delivery/strategy-selection-to-switch-latest.html
```

Expect `26/26 checks passed`. It confirms: reasonable size, single file with no `fetch`, external script, link, font or url, DATA embedded in its compact form, a data-as-of stamp per asset class, the only-if-better switching rule present, a static repository sample for each class (at most 30 strategies, all with different nets, full-day curves) and the repository button and sheet, the build timestamp embedded, every case belongs to a known class and product, **crypto and forex are kept separate (no strategy in both)**, wording rules, distinct net returns, no switch target that is, or clones, the selected strategy, every strategy has a curve, the closed-position filter wording matches what was applied (none by default), three scenarios, and the mobile-first markers. Any `FAIL` blocks delivery: fix the template or builder, rebuild, re-run.

Optional browser smoke test (the user never needs a server; this is only for testing):
1. `python -m http.server 8761 --bind 127.0.0.1` inside `epics/ep_062_product_delivery`, open `http://127.0.0.1:8761/<file>`.
2. Click Crypto and Forex, and step through product, scenario, hour and the four switch buttons for each, at a phone width (375 px, no horizontal scroll, bottom stage bar visible) and a desktop width (about 1100 px, stage buttons at the top, real tables); the console must show no errors; switching class must change the date, the product list and the header; in stage 1 each chart-legend value should equal the net in the table beside it.
3. Stop the server afterwards.

## Rules the page must keep

1. **Single file, no server.** Everything embedded; opens by double-click. Never add fetch calls, CDNs, web fonts or external images.
2. **Wording.** Say **"switch"** and **"closed positions"**. The word "trade" (also "trading") must not appear in visible text. The file name keeps `switch`.
3. **No look-ahead.** Every choice at a decision hour uses only the last snapshot at or before `HH:00:00` and closed positions up to then. Charts and "at decision" figures use values strictly before the decision minute. Anything after the decision appears only as what happened next in stage 3.
4. **Switch only when better.** The comparison targets are different strategies, so they can have a lower net than the selected one. "Always switch" and the one-off switch must therefore act only when the target's net (as known at that hour) is higher than the net of the strategy currently held; otherwise the page says "no switch" and holds. The page text must say so ("Switch, only when better"). The first row of the hour-by-hour table is a hold unless the target beats the selected strategy.
5. **Distinct net returns and a different strategy.** Strategies with the same net are clones: listed once, never used as alternatives. Every comparison target (best similar, opposite, overall, win rate) must be a different strategy with a different net from the selected one, even if it performs worse; when none exists the card says "none at this time" and no switch is made. Never fall back to the selected strategy. Ties go to the lowest model id.
6. **No closed-position filter.** Do not filter strategies by number of closed positions unless the user explicitly asks (`--min-closed N`). Net includes open positions, so a strategy with no closed positions can lead on floating profit; that is accepted. The page text must not claim a minimum that was not applied (verification checks this).
7. **Crypto and forex stay separate.** Selection, comparison, correlation, "All products" pooling, the "Does switching pay?" summary and the dates are all computed within one asset class. The switch only changes which class is displayed. Never pool or compare across classes; units and markets differ.
8. **Definitions on the page:** similar = same product, differs in exactly one of family, window, take-profit or stop-loss; opposite = five-minute equity changes correlate at -0.2 or lower with the selected strategy; overall = highest net; best win rate = highest share of winning closed positions. Selection scenarios: Top Net, Top Win Rate, Top Buy Sell.
9. **Honesty.** The page reports forward results even when switching loses, and says one day is a small sample. Do not tune the rules to make the result look better, and do not add investment advice, signals or forecasts. Keep the disclaimer.
10. **Mobile first.** The base CSS is the phone layout and wider screens are added with `min-width` queries (breakpoints 560 and 720 px): no horizontal scroll at 375 px; tables become stacked cards on phones (cells get `data-label` from the header); a fixed bottom bar switches stages 1, 2 and 3 on phones (the top stage buttons appear from 720 px); controls are 48 px tall with an earlier-hour and later-hour button beside the slider; a sticky bar keeps class, product, scenario and hour in view; charts are drawn at the real screen width so text stays readable and redraw on resize or stage change; text inputs are 16 px so phones do not zoom; the intro sits in a collapsed "How this works" section on phones. Keep all of this when editing the template, and check it at 375 px and about 1100 px.
11. **Timestamp and freshness.** The file name carries the build time, the file embeds it, and the header shows `Data as of <class> <time> · built <time>` so users know how fresh the data is.
12. **Repository sample is static and illustrative.** The sheet shows an evenly spread sample (24 per class, best to worst by end-of-day net, distinct nets only, no closed-position filter) with full-day curves every 15 minutes, never the whole repository, no sorting, search or paging. It states the real totals ("24 of N strategies, M with different results") and that selection never uses it. It must stay mobile first (2 cards across on phones, 3 from 720 px, 4 from 1000 px, 48 px close button, Escape closes). It is inside the file; do not link out to a platform page that needs a server.
13. **Keep the file small.** Curves keep one point per minute and only the first and last point of each flat run; case rows are short arrays with strategy names and products in one lookup, rebuilt by `hydrate()` in the template. Aim for about 3 MB with both classes (verification flags files over 6 MB). If you change the data layout, change the builder, the template's `hydrate()` and `verify_explorer.py` together.

## Deliver

- Send the timestamped file (not a copy you renamed by hand). The `-latest` copy is for the team's own use.
- Report to the user: data-as-of time and date for each class, products and cases, file size, verification result, anything unusual (empty early hours, products skipped, forex on an earlier date than crypto).
- **Sending is the user's action.** Do not email, upload or publish the file unless the user explicitly asks in the current conversation; then confirm the recipient or destination first.
- **Keep history. Never delete a previous timestamped build** (they are about 2 MB each). Users need the history of what was sent when. Only the `-latest` copy is overwritten. If a build was deleted by mistake, restore it with `--as-of` (below).

## Housekeeping (this repo)

- Add or update a workstream task file (`workstream/300_complete/claude/`, name `yyyymmdd_ep062_...md`) with the rebuild evidence: data-as-of time per class, case count, verification output.
- Commit only specific files (never `git add -A`; other sessions have uncommitted work).
- Template or builder changes: rebuild, re-run verification and the smoke test, then note the change in the task file and bump the version history above.

## Troubleshooting

| Symptom | Likely cause and fix |
|---|---|
| `No database URL` | Pass `--dsn`, set `SOURCE_DATABASE_URL`, or check the EP058 `.env`. |
| `No snapshots for <class> in the last 21 days` or `No recent snapshots for <class>` | That asset class has no recent data. Build the other class with `--product-type`. |
| `No qualifying data` | No snapshots that day. Pick another `--date`. |
| Forex shows an earlier date than crypto | Expected only when forex has no newer data (markets are closed at weekends). Each class uses its own newest day with data. Use `--date` to force one day. |
| Page shows the dim "No strategy has data at this time" notice | Early hours or an empty product; pick a later hour or another product. |
| Stage 1 list shorter than 6 | Several strategies shared the same net and were collapsed as clones. Expected. |
| Build is slow | Both classes take about 6 minutes. Use `--product-type` or `--products` for a quick check, then run the full build in the background. |
| File over about 6 MB | Too many products or the compact encoding was broken. Use `--products`, or check `compress_curve` and `compact_cases` in the builder. |
| Verification fails on wording | Search the template for "trade" or "trading" in visible text and change to "switch" or "closed positions". |
