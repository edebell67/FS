# Scenario engine v2 — status of the 25 items (2026-10-17)

Parent epic: EP057 (`epics/ep_057_sql_to_pgsql`); the arena side is EP052. Package: `epics/ep_057_sql_to_pgsql/scenario_engine_v2/`. Task files for this work are in `workstream/050_review/general` (not 300_complete: awaiting acceptance). Local commits only (not pushed): 08146ed0, c94ae7a2, d4633ce0, 106f8dc4, 667ca88e, 98261e91.
Task files: `workstream/050_review/general/20261016_15*_ep057_*.md` and `20261017_190000_ep057_997_arena_strategy_intelligence.md` (mirrored in `obs/Hermes Task Memory/workstream_mirror/`).

| # | Item | Status | Evidence / what is left |
|---|------|--------|-------------------------|
| 1–13 | Engine core (Page controller, tests, mutation tests, map/drift, version blocks, task files) | Done | Differential tests page JS (Node) vs Python on real :8765 data + synthetic; ~190 mutants killed (documented equivalents in `tools/mutants_page.py`); `check_drift.py` clean |
| 14 | Parallel headless instances (max 5, configurable) | Done | `runner/manager.py`, `tests/test_runner*.py` |
| 15 | Thin browser copy without embedded engine | Partly | Generated page `top10_5min_equity_curves_engine_client_v2.65.32.html`. Overlay/rotation engine and 8 no-network controllers run in Python. The other ~33 controllers still run in the page |
| 16 | Browser parity verification | Partly | Parity proven for the delegated parts (slice 1 + stage 1: 80/80 per controller, real-browser run). Not yet proven for the remaining controllers |
| 17 | Launch headless races from the browser | Done | `runner/static/launch_panel.js`, tests |
| 18 | Reporting dashboard | Done | `/dashboard` on :8766 |
| 19 | Deactivate the embedded version | Declined by you | Original left untouched; task `…998_deactivate_embedded_version` stays in backlog |
| 20 | Arena intelligence (top-N, clusters, spread signals) | Done | `engine/intelligence.py`, `runner/intel.py`, tests |
| 21 | Proactive delivery | Done | watches + `/v1/queries` provider, tests |
| 22 | Arena integration / agents launching races | Partly | Provider + opt-in `config.ep057_intelligence.toml` built; live `config.toml` unchanged. Full arena API run NOT done: Postgres :5432 needs a password I do not have. Run the suite yourself (command below) |
| 23 | Task 0 acceptance | Yours | Waiting for your acceptance |
| 24 | Superseded files | Done | recorded in task files |
| 25 | Cleanup | Done | |

## Left to do
1. **Stage 2 controller move** (activate/switch date/set ranking/refresh and the rest): needs a server-side per-page session that owns the data caches (ALL_CRITERIA_DATA, portfolio view caches, rule library, trade cache, portfolioModels), then a wrapper-vs-original differential per controller. Tried 2026-10-17: `applyChartLock` / `resetAutomaticRankSchedule` wrappers work except where the engine schedules timers (effects `setTimeout`/`clearTimeout` carry no callback identity, 19–80 of 80 cases fail on that). So the next step is engine-named timers (a callback registry) before any more controllers can move; generator support (EXTRAS) is in `tools/controller_wrappers.py`, the two are parked in comments. Original candidates with no fetch: `applyChartLock`, `resetAutomaticRankSchedule` (both already ported in `engine/page.py`; their DOM-shell lines must be copied into wrappers).
2. **Item 22 run:** `cd epics/ep_052_strategy_directory_agentic_trade_arena/lean_delivery/app && EP052_TEST_DATABASE_ADMIN_URL='postgresql://postgres:<password>@localhost:5432/postgres' python -m pytest tests -q`
3. **Item 23** acceptance (yours); **item 19** only if you change your mind.
4. Not done: per-agent quota on races; validating signal usefulness on history; speeding up the 38 ms / 0.5 s redraws.

## How completeness was tested
- `tests/test_parity_page_controller.py` (fast tier ~6 min; `RUN_SLOW=1` for 400 cases/method + all mutants), `tests/test_controller_wrappers.py`, runner/intel/arena-provider tests.
- `python tools/mutate_check.py` (mutants in `tools/mutants_page.py`), `python tools/check_drift.py <page>`.
