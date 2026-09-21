# Workstream Task: 5-Minute DNA Model Summary Snapshot Stored Procedure

**Task ID:** `20260919_190700_sp_snapshot_dna_model_summary_5min`  
**Start Date:** `2026-09-19 19:07:00`  
**Target Version:** `V20260919_1907`  
**Associated Files / Directories:**  
- Source DBs: SQL Server `tcp:EDS,1433/tradedb` and `tradedb_sim2`  
- Target DB: PostgreSQL `localhost:5432/tradedb`  
- SQL Scripts:  
  - `C:\Users\edebe\eds\db_scripts\dbo.tbl_dna_model_summary_snapshots_5min.Table.sql`  
  - `C:\Users\edebe\eds\db_scripts\dbo.sp_snapshot_dna_model_summary_5min.StoredProcedure.sql`  
- Master Export: `C:\Users\edebe\eds\workstream\20260919_190700_V20260919_1907_sp_snapshot_dna_model_summary_5min.sql`  
- Version File: `C:\Users\edebe\eds\TradeApps\breakout\fs\constants.py`  

---

## Check List of Changes

- [ ] **Task 1: Workstream Initialization & Version Bump**
  - [ ] Bump version in `TradeApps/breakout/fs/constants.py` to `V20260919_1907`.
  - [ ] Create lifecycle task in `workstream/100_todo/` and move to `workstream/200_inprogress/`.
- [ ] **Task 2: Snapshot Storage Table Design**
  - [ ] Design table `tbl_dna_model_summary_snapshots_5min` with schema:
    - `snapshot_id` (bigint identity PK)
    - `snapshot_timestamp` (datetime2(3) / timestamp)
    - `model` (varchar(50) / text)
    - `strategy_name` (varchar(64))
    - `strategy_family` (varchar(32))
    - `cum_net` (float / double precision)
    - `cum_alt_net` (float / double precision)
    - `cum_buy_net` (float / double precision)
    - `cum_buy_alt_net` (float / double precision)
    - `cum_sell_net` (float / double precision)
    - `cum_sell_alt_net` (float / double precision)
    - `open_trade_count` (int)
    - `closed_trade_count` (int)
    - `created_at` (datetime2(3) / timestamp default current_timestamp)
  - [ ] Create table in SQL Server `tradedb` and `tradedb_sim2`.
  - [ ] Create table in PostgreSQL `tradedb`.
- [ ] **Task 3: Stored Procedure Implementation (`sp_snapshot_dna_model_summary_5min`)**
  - [ ] Implement T-SQL stored procedure with 5-minute cadence gate or parameterized execution.
  - [ ] Aggregate from `combined_trades_closed` and `combined_trades_open` joined with `product_forex`.
  - [ ] Deploy procedure in SQL Server `tradedb` and `tradedb_sim2`.
  - [ ] Translate procedure to native PL/pgSQL and deploy in PostgreSQL `tradedb`.
- [ ] **Task 4: Integration with Supervisor (`sp_loop_create_trades_v2`)**
  - [ ] Add gated 5-minute call into `sp_loop_create_trades_v2` in SQL Server and PostgreSQL with `@skip_dna_summary_snapshot_5min` config flag.
- [ ] **Task 5: Verification & Lifecycle Completion**
  - [ ] Test execution in SQL Server `tradedb`, `tradedb_sim2`, and PostgreSQL `tradedb`.
  - [ ] Verify snapshot data rows populated with correct metrics.
  - [ ] Move task file to `workstream/300_complete/`.
  - [ ] Present completed checklist to user.

---

## Implementation Log
- **2026-09-19 19:07:00** - Workstream task initialized in `workstream/100_todo/`.
