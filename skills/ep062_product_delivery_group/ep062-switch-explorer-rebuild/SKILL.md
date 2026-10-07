---
name: ep062-switch-explorer-rebuild
description: Re-create the EP062 "Select. Compare. Switch." interactive web app on demand with up-to-date data, for crypto and forex (kept separate, chosen with an asset-class switch), including the hermes variant, a minimum-closed-positions option and the Join the Arena waitlist button. Use when asked to rebuild, refresh, update, regenerate, timestamp, restore or send a new version of the strategy selection / compare / switch explorer or its hermes version, or to build it for a different date, product, asset class or minimum. Produces ONE self-contained, timestamped html file (data embedded, no server, no data requests) that users open by double-clicking.
version: 1.6.1
---

# EP062 Switch Explorer: rebuild on demand

> VERSION HISTORY
> - v1.6.1 · 2026-10-07 · The hermes variant carries the Net | Alt net toggle too (hermes builder v1.4.0, verifier 14 checks, 7 MB limit); it opens on Net; an older single-basis source is wrapped and shows no toggle.
> - v1.6.0 · 2026-10-07 · Net | Alt net toggle: one file carries both return bases (net_return and alt_net_return) built from one fixed data cutoff; `--return-type both|net|alt` (default both); wording follows the basis; the hermes builder keeps the net basis; verification 28 checks; file about 5 MB with both classes on a full day (limit 7 MB).
> - v1.5.0 · 2026-10-06 · Delivery update: Join the Arena waitlist button in the main explorer (the one allowed external link, checked by the verifier, 27 checks); hermes variant build and verification documented (`--source`, any minimum 1 to 12); a class with nothing qualifying on its newest day steps back to the previous day; minimum-closed variants (`-min3`, `-min6`) and the "wait for a snapshot, then rebuild" pipeline; commit rules for generated builds; reporting checklist.
> - v1.4.0 · 2026-10-05 · History is kept: never delete a previous timestamped build. New `--as-of` option rebuilds how the data stood at a past time (history copies named `...-asof-YYYYMMDD-HHMM.html`).
> - v1.3.1 · 2026-10-05 · Closed-position filter removed (default `--min-closed 0`); page wording follows the stored value; verification checks for stale filter wording (26 checks).
> - v1.3.0 · 2026-10-05 · "Browse the strategy repository" link opens a static, evenly spread sample of the repository (24 per class) as full-day equity curves; verification 25 checks.
> - v1.2.0 · 2026-10-05 · "Always switch" now switches only when the other strategy's net is higher than the one held; default date is the newest day with any data (`--min-hours 1`); verification 22 checks.
> - v1.1.0 · 2026-10-05 · Forex added with a Crypto | Forex switch (never pooled); each class has its own date and data-as-of time; timestamped output with a `-latest` copy; compact data encoding; verification 21 checks.
> - v1.0.3 · 2026-10-04 · "All products" option (default) pools every loaded product for selection and comparison.
> - v1.0.2 · 2026-10-04 · Mobile first layout rules added; verification 17 checks.
> - v1.0.1 · 2026-10-04 · Comparison targets must be a different strategy with a different net (no fallback to the selected one); verification 14 checks.
> - v1.0.0 · 2026-10-04 · First version: rebuild script, verification script, delivery and wording rules.

The explorer is a three-stage page: **1 Strategy selection** (a scenario picks one strategy), **2 Compare** (best similar, best opposite, best overall, best win rate), **3 Switch** (replay what happened after switching, including "always switch, only when better" hour by hour). It shows equity-curve charts of the selected strategies in stages 1 and 2, and the replay in stage 3. An **Asset class** switch at the top (Crypto | Forex) chooses which market is shown. A **Browse the strategy repository** button opens a full-screen sheet with a static sample of the repository as equity-curve cards. A **Net | Alt net** toggle (Return basis) switches selection, comparison, charts, switching results, the repository sample and all wording between `net_return` and `alt_net_return`. A **Join the Arena waitlist** button opens the optional waitlist page.

## When to use

- "Rebuild / refresh / update the switch explorer", "send users the latest version", "timestamp it", "build it for forex / for date X / for product Y", "use a minimum of N closed positions", "generate the hermes version with the latest data", "restore the earlier build".
- Do not use for live dashboards, accounts, execution, advice or forecasts. The page is a historical, analytical replay.

## Where things live

All paths are under the repo root `C:\Users\edebe\eds`.

| Item | Path |
|---|---|
| Builder (source of truth) | `epics/ep_062_product_delivery/build_switch_explorer.py` |
| Page template (HTML, CSS, JS) | `epics/ep_062_product_delivery/switch_explorer_template.html` |
| Output, timestamped | `epics/ep_062_product_delivery/strategy-selection-to-switch-YYYYMMDD-HHMM.html` (add `-min3` / `-min6` when a minimum was used; `-asof-` for history rebuilds) |
| Output, newest copy | `epics/ep_062_product_delivery/strategy-selection-to-switch-latest.html` (only a plain default build refreshes it) |
| Verifier for the main explorer | `skills/ep062_product_delivery_group/ep062-switch-explorer-rebuild/scripts/verify_explorer.py` |
| Hermes variant builder, template, verifier | `epics/ep_062_product_delivery/hermes/build_hermes_version.py`, `switch_explorer_hermes_template.html`, `verify_hermes_version.py` |
| Hermes outputs | `epics/ep_062_product_delivery/hermes/strategy-selection-to-switch-hermes-YYYYMMDD-HHMM.html` |
| Older frozen evidence explorer (different product) | `epics/ep_062_product_delivery/strategy-directory-evidence-explorer-drilldown.html` |

Edit the template or builder for any change. Never hand-edit a generated html: the next rebuild overwrites it.

## Prerequisites

- Python 3 with `psycopg` installed.
- Read access to PostgreSQL `tradedb`. The builder takes `--dsn`, else env `SOURCE_DATABASE_URL`, else the EP058 settings (`epics/ep_058_strategy_intelligence_pg/hosted_directory/.env`). Never print or quote the connection string or any password.
- **PostgreSQL only, read-only.** Do not touch SQL Server. The builder only runs `select` statements on `tbl_dna_model_summary_snapshots_5min`, `product_forex` and `combined_trades_closed`.

## Rebuild the main explorer

```powershell
cd C:\Users\edebe\eds\epics\ep_062_product_delivery
python build_switch_explorer.py
```

A full build (both classes) takes about 6 to 8 minutes. Run it in the background and wait for the final `wrote ...` and `refreshed ...` lines (the monitor must tolerate that long). `--product-type crypto` alone takes about a minute.

Options:

| Option | Meaning |
|---|---|
| `--product-type both\|crypto\|forex` | Asset classes to include. Default `both`. |
| `--date YYYY-MM-DD` | Day to replay, applied to every class. Default: each class uses its own newest day with data. An explicit `--date` is never replaced. |
| (automatic fallback) | If a class has nothing that qualifies on its newest day (for example forex early in the day, when no strategy has enough closed positions yet), the builder steps back to the previous day with data. The page shows each class's own date, so crypto can be today and forex yesterday. Say so when reporting. |
| `--min-hours 1` | Hours of snapshots a day needs when picking the default date. Keep 1. |
| `--return-type both\|net\|alt` | Default **both**: one file with the toggle (opens on Net). `net` or `alt` build a single basis (alt-only files are named `...-alt.html`, never refresh `-latest`, and open on Alt net). Both bases read the same data: nothing newer than the moment the build started. |
| `--min-closed N` | Minimum closed positions a strategy needs to qualify. **Default 0 = no filter.** Only set it when the user asks (they have asked for 6 and for 3). The value is stored in the file and all page wording follows it. Write such builds with `--out strategy-selection-to-switch-<stamp>-min<N>.html` so they are never confused with the unfiltered build; `--out` does not touch `-latest`. |
| `--products avax,btc` | Comma list of products; only with a single `--product-type`. |
| `--first-hour 3` | Earliest decision hour. |
| `--as-of ...` | Rebuild as the data stood at a past time (history or a restore): `--as-of "2026-10-05 15:41"` for every class, or `--as-of "crypto=...,forex=..."`. Combine with `--date` and the `--min-closed` the original used. Named `...-asof-YYYYMMDD-HHMM.html` unless `--out`; does not touch `-latest`; the header says it was rebuilt from stored data. |
| `--out path.html` | Output file. With `--out` no `-latest` copy is made. |
| `--no-latest` | Do not refresh the `-latest` copy. |
| (automatic) | Inside each class, when two or more products are loaded the page gets an **All products** option (the default), pooling that class only. |

Output naming: without `--out` the builder writes `strategy-selection-to-switch-YYYYMMDD-HHMM.html` and refreshes `strategy-selection-to-switch-latest.html`. The build time is inside the file too: a `generated` meta tag, a leading html comment and the visible header stamp (`Data as of Crypto ... · Forex ... · built ...`).

If a product has no snapshots on the day it is skipped (forex has many `_c`/`_s` products that are often empty). If a whole class has nothing it is left out and the switch hides. If nothing qualifies at all, the builder stops with an error.

### When the user says "wait for the 12:00 snapshot, then rebuild"

Do not guess. Poll the database for `max(snapshot_timestamp)` on the day (it must pass the hour plus one minute, so the hour's cut-off exists), then run the builds in one background script and monitor its log: poll with a 20 second sleep inside the script, build the base, then the hermes version, then write `PIPELINE DONE` to a log. Report the as-of times from the log.

## Hermes variant (separate UI, same data)

The hermes version never queries the database; it is built from a main explorer build that has a minimum of closed positions (1 to 12). To get it with the latest data:

```powershell
cd C:\Users\edebe\eds\epics\ep_062_product_delivery
python build_switch_explorer.py --min-closed 3 --out strategy-selection-to-switch-<YYYYMMDD-HHMM>-min3.html
python hermes\build_hermes_version.py --source strategy-selection-to-switch-<YYYYMMDD-HHMM>-min3.html
python hermes\verify_hermes_version.py hermes\strategy-selection-to-switch-hermes-<built>.html
```

- Without `--source` the hermes builder uses the newest `*-min?.html` in the parent folder. Use `--source` to be explicit.
- The number word in the page copy ("at least three closed positions") comes from the source's `min_closed` via the `__MIN_WORD__` placeholder in the hermes template. Never hard-code a number word or a digit minimum in either template.
- The hermes page keeps its own guided example, honesty wording and the single waitlist button, and carries the same **Net | Alt net toggle** as the main explorer (both bases from the source are kept, it opens on Net, the tab title and the "What do net, win rate ... mean?" panel follow the basis, and the guided example keeps the chosen basis). The verifier (14 checks) enforces all of it. The history-copy label only appears when the source itself was an `--as-of` rebuild.
- It refuses to overwrite a build from the same minute, and refuses a source without both asset classes.

## Verify (always, before sending)

```powershell
cd C:\Users\edebe\eds
python skills/ep062_product_delivery_group/ep062-switch-explorer-rebuild/scripts/verify_explorer.py epics/ep_062_product_delivery/<the build>.html
```

Expect `28/28 checks passed` (the hermes verifier has its own 14). It confirms: reasonable size; **exactly one external link, the secure Join the Arena waitlist button, and nothing else** that could fetch (`fetch`, external script, link, font or url); DATA embedded in its compact form; a data-as-of stamp per asset class; the build timestamp embedded; every case belongs to a known class and product; **crypto and forex are kept separate (no strategy in both)**; wording rules; distinct net returns; no switch target that is, or clones, the selected strategy; every strategy has a curve; the closed-position filter wording matches what was applied; three scenarios; a static repository sample per class with the button and sheet; the only-if-better switching rule; **both return bases present with identical case coverage, the toggle, its note and the forex warning**; and the mobile-first markers. Any `FAIL` blocks delivery: fix the template or builder, rebuild, re-run. (Builds made before the waitlist button was added fail only that one check; that is expected.)

Optional browser smoke test (the user never needs a server; this is only for testing):
1. `python -m http.server 8761 --bind 127.0.0.1` inside the folder holding the file, open `http://127.0.0.1:8761/<file>`.
2. Click Crypto and Forex, and step through product, scenario, hour and the four switch buttons for each, at a phone width (375 px: no horizontal scroll, bottom stage bar visible) and a desktop width (about 1100 px: stage buttons at the top, real tables); the console must show no errors; switching class must change the date, the product list and the header; the waitlist button must be one link opening in a new tab.
3. Stop the server afterwards.

## Rules the page must keep

1. **Single file, no server, no data requests.** Everything embedded; opens by double-click. Never add fetch calls, CDNs, web fonts, external scripts or images. The only external reference allowed is the one waitlist link below, which loads nothing until a user taps it.
2. **Wording.** Say **"switch"** and **"closed positions"**. The word "trade" (also "trading") must not appear in visible text. The file name keeps `switch`.
3. **No look-ahead.** Every choice at a decision hour uses only the last snapshot at or before `HH:00:00` and closed positions up to then. Charts and "at decision" figures use values strictly before the decision minute. Anything after the decision appears only as what happened next in stage 3.
4. **Switch only when better.** Comparison targets are different strategies and can have a lower net than the selected one. "Always switch" and the one-off switch act only when the target's net (as known at that hour) is higher than the net of the strategy currently held; otherwise the page says "no switch" and holds. Hour-by-hour rows are tagged switch or hold.
5. **Distinct net returns and a different strategy.** Strategies with the same net are clones: listed once, never used as alternatives. Every comparison target must be a different strategy with a different net from the selected one, even if it performs worse; when none exists the card says "none at this time". Never fall back to the selected strategy. Ties go to the lowest model id.
6. **Minimum closed positions only on request.** Default is no filter; net includes open positions, so a strategy with no closed positions can lead on floating profit (accepted). When the user asks for a minimum, apply it with `--min-closed N`; every sentence in the page that mentions a minimum is generated from that value (rules, repository note, no-data and no-opposite messages). The page text must not claim a minimum that was not applied (verification checks the no-filter case).
7. **Crypto and forex stay separate.** Selection, comparison, correlation, "All products" pooling, the "Does switching pay?" summary and the dates are all computed within one asset class. The switch only changes which class is displayed. Never pool or compare across classes.
8. **Definitions on the page:** similar = same product, differs in exactly one of family, window, take-profit or stop-loss; opposite = five-minute equity changes correlate at -0.2 or lower with the selected strategy; overall = highest net; best win rate = highest share of winning closed positions. Scenarios: Top Net, Top Win Rate, Top Buy Sell.
9. **Honesty.** The page reports forward results even when switching loses, and says one day is a small sample. Do not tune the rules to make the result look better, and do not add investment advice, signals or forecasts. Keep the disclaimer.
10. **Mobile first.** The base CSS is the phone layout and wider screens are added with `min-width` queries (560 and 720 px): no horizontal scroll at 375 px; tables become stacked cards on phones; a fixed bottom bar switches stages on phones; controls are 48 px tall with earlier/later hour buttons; a sticky bar keeps class, product, scenario and hour in view; charts are drawn at the real screen width and redraw on resize or stage change; inputs are 16 px; the intro is a collapsed "How this works" section on phones. Check at 375 px and about 1100 px.
11. **Timestamp and freshness.** The file name carries the build time, the file embeds it, and the header shows `Data as of <class> <time> · built <time>`.
12. **Repository sample is static and illustrative.** An evenly spread sample (24 per class, best to worst by end-of-day net, distinct nets only, respecting any minimum) with full-day curves, never the whole repository, no sorting, search or paging; it states the real totals and that selection never uses it; two cards across on phones, three from 720 px, four from 1000 px; Escape closes. It lives inside the file.
13. **Join the Arena waitlist button.** Exactly one `<a class="waitlistButton" href="https://thetechprinciple.com/waitlist/" target="_blank" rel="noopener noreferrer">` in the "Want updates about the Arena?" box below the intro, with the wording "The optional waitlist is hosted separately from this historical explorer." and "Joining does not guarantee live access." Never add another external link, tracking or form. Keep it in both the main template and the hermes template.
14. **Net | Alt net toggle.** Both bases are in the one file; every word that says net comes from the chosen basis (`NW()`, `NWC()`, `scenName()` and the `nw` / `Nw` spans), never hard-coded. Open on Net. Product, scenario and hour stay put when flipping. Both bases must cover exactly the same cases (checked). Show the definition note under the toggle (alt net = the platform's counterfactual measure, what a reversed position would have returned after the same cost) and, for forex, "For forex it is not a simple mirror of net return." Evidence behind that note (combined_trades_closed, all history): crypto net + alt is a near constant -40 on 1.86 million positions (correlation -1.000, every product, both months), so alt is net reversed minus a fixed cost; forex is not (net + alt averages -28 with a standard deviation of 48; per-strategy averages correlate +0.35). Never describe alt as a pure mirror for forex. Do not use the word "trade" in the alt definition.
15. **Keep the file small.** Curves keep one point per minute and only the first and last point of each flat run; case rows are short arrays with strategy names in one lookup, rebuilt by `hydrate()`. Aim for about 3 MB per basis (about 5 MB for a full day, both bases, both classes; verification flags files over 7 MB). If you change the data layout, change the builder, the template's `hydrate()` and `verify_explorer.py` together.

## Deliver

- Send the timestamped file (not a copy renamed by hand). The `-latest` copy is for the team's own use.
- **Report to the user:** file name; data-as-of date and time for each class (and say if one class fell back to an earlier day and why); the minimum closed positions applied; products and cases; file size; verification results (main and hermes); anything unusual (empty early hours, products skipped).
- **Sending is the user's action.** Do not email, upload or publish a file unless the user explicitly asks in the current conversation; then confirm the recipient or destination first.
- **Keep history. Never delete a previous timestamped build** (about 2 to 3 MB each). Only the `-latest` copy is overwritten. A build that was never delivered and is plainly wrong (for example a mislabelled test build made minutes ago) may be removed, but say so. Restore a lost build with `--as-of`.

## Housekeeping (this repo)

- Add or update a workstream task file (`workstream/300_complete/claude/`, name `yyyymmdd_ep062_...md`) with the evidence: data-as-of time per class, case count, minimum applied, verification output. The `workstream/` folder is gitignored, so these notes are not committed.
- Commit only specific files (never `git add -A`; other sessions have uncommitted work). Source (builder, template, hermes scripts, skill) is committed on request. Generated builds are committed only when the user asks; first scan them for secrets (connection strings, passwords, tokens) and remind the user that the repository is public and the files contain strategy performance data. Do not push unless asked.
- Template or builder changes: rebuild, re-run verification and the smoke test, then note the change in the task file and bump the version history above.

## Troubleshooting

| Symptom | Likely cause and fix |
|---|---|
| `No database URL` | Pass `--dsn`, set `SOURCE_DATABASE_URL`, or check the EP058 `.env`. |
| `No snapshots for <class> in the last 21 days` or `No recent snapshots for <class>` | That asset class has no recent data. Build the other class with `--product-type`. |
| `No qualifying data` | No snapshots that day. Pick another `--date`. |
| Forex shows an earlier date than crypto | Forex had no strategy meeting the minimum on its newest day yet (early in the day, or markets closed). Expected; it steps back automatically. Rebuild after more positions have closed to move it forward. |
| Hermes build says "Source must hold both asset classes" | The base build left a class out. Use the default fallback (no `--date`), or fix the date. |
| `FAIL exactly one secure external link` | The waitlist box is missing, duplicated, or its anchor lost `target="_blank"` or `rel="noopener noreferrer"`. Restore it in the template and rebuild. Builds from before the button existed fail only this check. |
| Page shows the dim "No strategy has data at this time" notice | Early hours or an empty product; pick a later hour or another product. |
| Stage 1 list shorter than 6 | Several strategies shared the same net and were collapsed as clones. Expected. |
| Build is slow | Both classes take 6 to 8 minutes. Use `--product-type` or `--products` for a quick check, then run the full build in the background. |
| File over about 7 MB | Too many products or the compact encoding was broken. Use `--products`, or check `compress_curve` and `compact_cases` in the builder. |
| Verification fails on wording | Search the template for "trade" or "trading" in visible text and change to "switch" or "closed positions". |
