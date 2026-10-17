# Stage 2 design — server-side page session and named timers (EP057, 2026-10-17)

Status: DESIGN ONLY (not built). Stage 1 (8 no-network controllers) is built and tested; see STATUS_25_items.md.

## Why stage 1's approach stops here
Stage 1 sends the whole page state with each command and applies the answer. That works while a controller needs no network and leaves no timer behind. The remaining ~33 controllers either
1. fetch (activate, switch date, set ranking, refresh live data, load portfolio data, point-in-time selection / history), or
2. schedule timers whose callback is a Python closure (`Page._timeout`, engine/page.py:108) — e.g. the 180 ms point-in-time debounce in `schedule_point_in_time_selection`. The engine is stateless per request, so a closure cannot outlive the request.

## Design
**A. Named timers.** Replace closures with `("setTimeout", ms, name, args)` effects. The page replays them as `setTimeout(() => __engineCommand('timer', [name, args]), ms)` and keeps the handle in the page (clearTimeout effects name the timer: `("clearTimeout", name)`). `Page.timer(name, args)` dispatches to a registry: `pit_selection(at)`, `model_search(...)`, `live_refresh()`, `hourly_report()`. Each existing timer variable in the page (`pointInTimeDebounceTimer`, `modelSearchTimer`, `liveRefreshTimer`, `hourlyReportTimer`, `portfolioViewRefreshTimer`) maps to one name.

**B. Page session (server side).** `runner/session.py`: one `PageSession` per browser tab, holding `DataClient` caches (ALL_CRITERIA_DATA, portfolio view caches, rule library, trade cache, portfolioModels). Commands carry a session id and send only the small UI state; the answer returns state *diffs* plus changed cache slices the DOM needs. Non-ported writers of those caches (found by scan): `restoreLiveChartCache`, `init`, `renderPortfolioTabs`, `setupEventListeners`, `syncLivePortfolioScreenState`, `renderCards` (pins), model search — each becomes a command or a cache-sync call.

**C. Fetching.** Inside a command the engine uses `DataClient` with the real :8765 client (as headless races do); the page never fetches for delegated controllers. Request ordering semantics (`Pending`, issue-order application) are already ported and tested.

## Order of work (each step: wrapper-vs-original differential 80/80 + mutants + real-browser exercise before the next)
1. Named timers (A) with `applyChartLock`, `resetAutomaticRankSchedule` (already prepared, parked) — the 61/80 and 0/80 results in the last run are the baseline.
2. Session + cache diffs (B) with `switchDate`, `setRankingCriteria`.
3. `activatePortfolio`, `loadPortfolioData`, `refreshLiveData`, point-in-time selection and history.
4. Remaining controllers; then item 15's "no embedded engine" check (all rule-path and controller code removed from the generated page).

## Risks
- Timer ordering vs in-flight requests (the harness must model timer firing between fetch completions).
- Payload size of cache diffs for 2000-model days; measure before choosing diff granularity.
- Live mode stays refused headless; the page keeps its own live-mode prelude (see `applyChartLock` EXTRAS).
