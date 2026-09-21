# Epic: SQL Server to PostgreSQL Migration & Trade Replay Engine
**Epic Path:** `C:\Users\edebe\eds\epics\ep_057_sql_to_pgsql`  
**Date:** `2026-09-20`  
**Database:** `tradedb` (PostgreSQL 17 `localhost:5432` / SQL Server `tcp:EDS,1433`)  

## Overview
This epic contains the complete set of artefacts used to establish schema parity, create objects in PostgreSQL, execute cross-database migrations from SQL Server, and run tick/trade replays natively in PostgreSQL.

---

## Folder Organization & Preserved Artefacts

### 1. `trade_replay_runners/`
PostgreSQL-backed trade replay and loop execution scripts:
- **`pg_historical_tick_replay_runner.py`**: Multi-day sequential tick price feeder and trade replay runner. Feeds ticks, evaluates breakout rules, manages open positions, logs 5-minute snapshots, and triggers EOF liquidation and associate deactivations.
- **`pg_loop_runner_031.py`**: Core PostgreSQL strategy execution loop for active breakout strategies.
- **`pg_loop_runner_031_sim2.py`**: PostgreSQL simulation loop runner targeting `tradedb_sim2`.
- **`pg_replay_sim2_runner.py`**: Dedicated replay simulation runner for PostgreSQL sim environments.
- **`price_diff_pg.py`**: High-frequency price delta and spread computation engine on PostgreSQL.

### 2. `db_objects_ddl/`
Schema definitions for PostgreSQL tables and views:
- **`create_combined_trades_closed_arc_pg.sql`**: DDL for archived closed trades table in PostgreSQL.
- **`alter_combined_trades_closed_arc_pg.sql`**: Column extensions and constraint updates.
- **`create_combined_trades_open_snapshot_pg.sql`**: Periodic open trades snapshot schema.
- **`create_zone_distribution_snapshots_pg.sql`**: Zone distribution telemetry logging schema.
- **`create_pgsql_linked_server.sql`**: SQL Server linked server configuration (`PGSQL_TRADEDB`) via ODBC.
- **`test_pgsql_linked_server.sql`**: Connectivity and query verification script for linked server.
- **`drop_pgsql_linked_server.sql`**: Cleanup script for linked server definitions.

### 3. `data_migration_procs/`
Stored procedures for automated cross-database sync:
- **`sp_sync_combined_trades_closed_arc_to_pgsql.sql`**: Incremental push of closed trades to PostgreSQL via `OPENQUERY`.
- **`sp_sync_combined_trades_open_snapshot_to_pgsql.sql`**: Periodic open positions synchronization.
- **`sp_sync_zone_distribution_snapshots_to_pgsql.sql`**: High-frequency zone telemetry sync to PostgreSQL.

### 4. `api_and_admin/`
Backend services interfacing with PostgreSQL:
- **`admin_api_pg.py`**: Administrative endpoints for managing model activations, parameters, and feeds in PostgreSQL.
- **`trade_viewer_api.py`**: Flask API feeding the Breakout Trade Viewer dashboards directly from PostgreSQL views.

### 5. `dashboards_and_uis/`
Interactive HTML/JS dashboards and analytical UIs powered by the new PostgreSQL schemas:
- **`mobile_winrate_replay_dashboard.html`**: Mobile-friendly strategy replay UI with Win Rate slider (>= X%, default 100%), 5-min snapshot equity curves, animated playback scrubber bar, and arbitrary baseline time initialization (e.g. delta since 03:00 am).
- **`top10_5min_equity_curves.html`**: Continuous 5-day multi-line equity curves for the Top 10 models with card isolation and hover inspection.
- **`top5_high_freq_directional_split.html`**: Top 5 high-frequency models with directional Long vs Short sub-ledgers.
- **`associates_hourly_directional_split.html`**: Hourly #1 associate models directional performance dashboard.
- **`all_dates_hourly_directional_split.html`**: Multi-day hourly leader matrix with directional splits.
- **`hourly_leaders_directional_split.html`**: Buy Net vs Sell Net split charts for hourly champions.
- **`hourly_leaders_equity_curves.html`**: Multi-date hourly leaders progression viewer.
- **`dna_201060_equity_curve.html`**: Dedicated granular equity curve for model DNA_201060.

### 6. `plans_and_specs/`
Historical architecture and migration plans:
- **`20260305_1800_V20260305_1800_SQL_TO_PG_MIGRATION.md`**: Initial parity and migration roadmap.
- **`20260121_1451_V20260121_1450_PGSQL_PNL_PERFORMANCE_AND_LIVE_FIX.md`**: PostgreSQL view performance tuning and live update architecture.
