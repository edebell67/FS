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

## Revision 2026-10-18 — fetching controllers use begin / finish commands, not a server session
Found while reading `refreshLiveData` (page line ~1960 / `Page.begin_refresh_live_data`): the original awaits a fetch in the middle of the function and its stale-response guards (`refreshSequence`, requested filters) compare state from *before* and *after* the await. One synchronous `/engine/call` per controller (the stage 1 shape) would
1. remove that await — the guards can never fire in the browser, so races the original handles are no longer exercised, and
2. block the page on a synchronous XHR for the whole fetch (the live-day request is the slow one).

So the session idea (B above) is replaced for fetching controllers by a **two-phase protocol**, which mirrors the engine's own `Pending` model (`begin_*` issues, `finish()` applies):
- `begin_<x>(args, state)` → `{requests: [url…], ctx}`; the engine records the sequence bump etc. in the returned state. `ctx` = the values the closure captured (seq, requested filters, target date) — the page keeps it and sends it back.
- The page issues the requests with its own `fetch` (non-blocking, keeps `window.__ep057EarlyChartRequest` and browser caching) and awaits them.
- `finish_<x>(ctx, responses, state)` runs with the page's CURRENT state, so the guards compare the right things, and returns state + cache writes (`ALL_CRITERIA_DATA` entries, `PORTFOLIO_VIEW_CACHE`) + effects.
- Controllers with nested fetches (`refreshLiveData` → `loadPortfolioData`, `switchDate`) loop: finish may return more `requests` plus a new ctx; the page repeats until `done`.
- The page stays the owner of the data caches (no server session); the engine gets only the cache slices a step reads and returns the entries it writes. This removes the session risk and the payload-size risk from the earlier design.

Test method per controller: the existing differential harness already records the fetch order and responses from the original; extend wrapper mode so the page-side loop is the thing under test (begin → fetch stub → finish) and compare final state + ordered effects + fetch URL sequence against the original. Order: `refreshLiveData` (one round + optional portfolio load), `loadPortfolioData`, `setRankingCriteria`, `switchDate`, `activatePortfolio`, then the rest.

Cost estimate: protocol + harness change ≈ the largest single piece; each controller afterwards is mostly mechanical (split Page method at the await, add ctx). Not started.

## Final revision 2026-10-18 — staged controllers (this is what was built; it supersedes the session and the begin / finish protocol above)
Status: BUILT, verified (items 15 / 16 of STATUS_25_items.md). `engine/twophase.py` (begin / finish for refresh_live_data) is kept and still tested but is no longer used by the browser copy.

**Principle.** The page keeps the data layer (HTTP and the page-owned caches); the engine owns the controller logic around it. A controller is split at each `await` into stages (`engine/page.py`: `Await`, `STAGES`, `run_stage`). A stage runs on the page's CURRENT state and answers either a result or `Await(fn, args, ctx, next, ...)`: "await this page function, then call me again at stage `next` with its result". The page shell (`tools/controller_wrappers.py`, `__drive` / `__apply` / `__resume`) awaits the named page function, takes a fresh snapshot, and resumes. Stale-response guards therefore compare real before / after state, exactly as the original does, with no payload shipped to the engine.

**Await flavours.** `catch` (a failure is reported as `{error}` instead of propagating); `sync` (call a synchronous page function and resume in the same turn: awaiting it would let other async work slip in); `fire` (start without waiting; with `handle` keep the promise); `attach` (run a later stage when a kept promise settles: a detached `.then`). `_call(fn)` asks the page to call a function at the end of the stage. `view_with(name, *args)` carries the arguments of a view call (setLiveBadge, scheduleLiveChartCacheFallback). `spawn` (command answers only): un-awaited work (the point-in-time lookups) = the engine does the part before the request in place and the page runs the fetch and the resume stage.

**What stays in the page.** See `tools/check_thin_boundary.py` BOUNDARY. LIVE / LIVE_ALT portfolios place orders: the engine refuses them (`LivePortfolioRefused` → `needsNetwork`) and the page runs `__original_activatePortfolio`; `syncLivePortfolioScreenState` stays in the page and the engine resumes after it.

**Rules learned.** A stage must not call a delegated function that may want the network (applyPortfolioViewConfig, schedulePointInTimeSelection): hand it to the page as an Await (sync) or `_call`, because a stage cannot fall back midway. Verify against the ORIGINAL page's JS on the real event loop, not against the Python event-loop model (it is only an approximation in failure paths).

