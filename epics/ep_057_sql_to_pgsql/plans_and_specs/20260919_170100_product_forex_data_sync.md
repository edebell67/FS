# Workstream Task: Synchronize product_forex Data from SQL Server tradedb to PostgreSQL tradedb

**Task ID:** `20260919_170100_product_forex_data_sync`  
**Start Date:** `2026-09-19 17:01:00`  
**Target Version:** `V20260919_1701`  
**Associated Files / Directories:**  
- Source DB: SQL Server `tcp:EDS,1433/tradedb.dbo.product_forex`  
- Destination DB: PostgreSQL `localhost:5432/tradedb.public.product_forex`  
- Version File: `C:\Users\edebe\eds\TradeApps\breakout\fs\constants.py`  

---

## Check List of Changes

- [ ] **Task 1: Version Constant & Workstream Setup**
  - [ ] Bump version in `TradeApps/breakout/fs/constants.py` to `V20260919_1701`.
  - [ ] Create lifecycle task in `workstream/200_inprogress/`.
- [ ] **Task 2: Extraction & Batch Insertion**
  - [ ] Extract all 12,514 rows from SQL Server `dbo.product_forex`.
  - [ ] Batch insert records into PostgreSQL `public.product_forex` preserving boolean conversions and null safety.
- [ ] **Task 3: Verification & Parity Check**
  - [ ] Confirm row count match (MSSQL 12,514 == PG 12,514).
  - [ ] Verify sample records and distribution (e.g. `trade_freq = 98` DNA_2xxxxx models).
  - [ ] Move task file to `workstream/300_complete/`.
  - [ ] Report completion with check boxes.

---

## Implementation Log
- **2026-09-19 17:01:00** - Workstream task initialized in `workstream/200_inprogress/`.
