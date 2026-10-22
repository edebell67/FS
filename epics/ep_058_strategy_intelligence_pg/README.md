# EP058 Strategy Intelligence (PostgreSQL)

## Version history

- 0.3.0 (2026-09-26): Local `ep058_intel` database created and populated; all intelligence query endpoints tested.
- 0.2.0 (2026-09-26): Dashboard API layer - an endpoint for every function on the ep_057 top10_5min_equity_curves.html page.
- 0.1.0 (2026-09-26): Scaffold. Code copied from EP049 `hosted_directory/` (no `.env`, no runtime state) as the PostgreSQL-sourced twin, following the SQL Server -> PostgreSQL move in EP057. Nothing run or verified yet.

Twin of `ep_049_strategy_intelligence`, sourcing from PostgreSQL `tradedb` (see `ep_057_sql_to_pgsql`) instead of SQL Server. Same intelligence query API, EP052 Arena provider (`app/arena_provider.py`) and architecture rules as EP049 - read its README for those.

## Status / open items

Done 2026-09-26:
- [x] Ported EP051's PG local-source shim (`source_connection`, T-SQL rewrite) into `app/repository.py` 1.13.0 and EP051's `LOCAL_SOURCE`/`SOURCE_DATABASE_URL`/`RUNTIME_DIR` settings into `app/config.py` 1.4.0.
- [x] `.env` (gitignored) created; app boots on port 8149 (EP049 is 8049). 54 tests pass (pytest needs `--basetemp` outside `%TEMP%\pytest-of-edebe`, which is access-denied).
- [x] `/api/intelligence/query/schema` serves 200.

Finding: EP049's app cannot read the local source directly. Its query endpoints return 503 "Intelligence repository is not configured" unless `DATA_BACKEND=postgres` with a `DATABASE_URL` pointing at a repository database populated by EP051's snapshot pipeline (`sync/export_snapshot.py` -> `sync/publish_snapshot.py` -> `/internal/snapshots`). The `LOCAL_SOURCE` shim only helps that export step, not this app.

Open:
- [ ] Decide the target repository DB (a new local PG database, e.g. `ep058_intel`, vs the hosted Render DB) and create its schema.
- [ ] Export from `tradedb` (EP051 `export_snapshot.py`, `LOCAL_SOURCE=postgres`) and publish into it.
- [ ] Set `DATA_BACKEND=postgres` + `DATABASE_URL` in `.env`, then run the query endpoints and compare against EP049 on the same date range; record in `evidence/`.
- [ ] `deploy/render.yaml` is an unedited EP049 copy - rename service and DB before use.
- [ ] Workstream task file per repo rule.

## Dashboard API layer (0.2.0)

Every function on `ep_057_sql_to_pgsql/dashboards_and_uis/top10_5min_equity_curves.html` (v2.30.0) now has an endpoint here, reading PostgreSQL `tradedb` via `SOURCE_DATABASE_URL` (not `DATABASE_URL`). Catalogue is also published under `dashboard_api` in `GET /api/intelligence/query/schema`.

| Page function | Endpoint |
|---|---|
| live scenarios, product/type/family filters, 10/20/30 limit, Touched #1, Top5 by family, TP/SL scenarios | `GET /api/live_day`, `GET /api/scenarios` |
| getScenarioCandidates / getEligibleModels (win-rate slider, filters, Net/Alt) | `POST /api/scenario_candidates` |
| ribbon deltas, baseline re-centering, replay head | `POST /api/ribbon`, `POST /api/replay_frame` |
| tri-split B/S/X overlay, trade values, flip result, daily target | `POST /api/overlay_signals` |
| Total Net leader rotation | `POST /api/leader_rotation` |
| Multi-Split rotation | `POST /api/multi_split_rotation` |
| named portfolios (create/delete/merge/add/remove, max 10) | `/api/portfolios*`, `POST /api/portfolio_merge` |
| similar-strategy portfolios | `GET /api/similar_strategies`, `POST /api/portfolio_from_similar` |
| strategy catalogue | `GET /api/strategy_catalog` |
| trades modal | `GET /api/model_trades` |
| hourly family exit report | `GET /api/hourly_family_report` |
| UI-only (theme, collapse, chart drawing, table sorting, scrubber speed) | no endpoint |

Code: `app/dashboard_queries.py` (vendored ep_057 query builders), `app/dashboard_engine.py` (Python port of the client-side logic), `app/dashboard_api.py` (routes; portfolios in SQLite `runtime/dashboard_portfolios.sqlite`).

Verification 2026-09-26: `live_day` (2 param sets), `strategy_catalog`, `hourly_family_report` payloads md5-identical to the running ep_057 server on :8765; leader rotation, multi-split and overlay signals/trades match the page's own JS run in node on the same data for 3 parameter sets; 59 tests pass. Not verified: `similar_strategies`/`model_trades`/`portfolio_day` payload parity, ribbon/replay_frame against the page's rendered numbers, portfolio endpoints beyond put/list/delete.

## Local repository database `ep058_intel` (0.3.0)

- Created on local PG (`localhost:5432`), migrations 001-006 from EP051 applied plus `hosted_directory/migrations/008_strategy_id_pattern.sql` (tradedb ids are lowercase/underscored). Migration 007 (creates cluster role `ep051_retention_owner`) deliberately NOT applied.
- Runtime role `ep058_app` (LOGIN, NOSUPERUSER, NOBYPASSRLS, non-owner) created because the app refuses to start as a superuser/owner. Password only in gitignored `hosted_directory/.env` (`DATABASE_URL`; `OWNER_DATABASE_URL` for migrations).
- Populated from `tradedb` via `sync/export_snapshot.py --history-limit 100` then `PostgresRepository.promote()`: snapshot `dna-20260926T170057Z-d19cbe51bd98`, 2000 strategies, 200000 return-series points, 2000 profiles. Full history (841,417 points) exceeds the snapshot contract's 250,000 cap, hence the limit; time-travel/regime results only see each strategy's latest 100 trades.
- Vendored `repository.py`, `contracts.py`, `intelligence/*` re-synced to EP051's newer versions (strategy_id pattern `(?i)^DNA_[A-Za-z0-9_]+$`, `max_points`).
- Bug fixed in `app/main.py` `cached_points`: it re-read every strategy's curve from the DB for each strategy (O(N^2) on PostgreSQL), so `timetravel` never finished (>15 min). It now reads the TTL-cached curves: `timetravel` 21s, `timetravel/series` 36s. EP049's own copy has the same flaw.

Query endpoint results 2026-09-26 (port 8149): search 200 (0 matches for win_rate>=0.8 & >=30 trades - not independently checked), chain 200 (8), top-performers 200, time-window 200 (0 matches), timetravel 200, timetravel/series 200, regime/similar-days 200 after `python -m sync.warm_regime_shape_index --instrument AUD` (~7 min per instrument; other instruments not warmed). 59 tests pass. Not done: comparison against EP049 results; Arena provider (`/v1/*`) not exercised here.

Parity check vs :8765 (2026-09-26, later): live_day (incl. family/limit params), portfolio_day, similar_strategies, model_trades (2 param sets), strategy_catalog (2 dates), hourly_family_report (crypto, forex+family, today) all md5-identical. This caught real drift: ep_057 changed the hourly report's crypto handling at 17:20 after the first vendoring, so `app/dashboard_queries.py` is now generated: `python -m sync.vendor_dashboard_queries` (re-vendor) / `--check` (drift, exit 1). `dashboard_engine.py` remains a hand port of the page JS (no automatic drift check).
