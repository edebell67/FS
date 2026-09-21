# Workstream Task: Bottom-Up Functional PL/pgSQL Translation of Core Trading Engine

**Task ID:** `20260919_160000_core_engine_plpgsql_translation`  
**Start Date:** `2026-09-19 16:00:00`  
**Target Version:** `V20260919_1600`  
**Associated Files / Directories:**  
- Plan: `C:\Users\edebe\.gemini\antigravity\brain\6aed791c-b3c5-4ab4-a571-c23206db4462\implementation_plan.md`  
- Output Script: `C:\Users\edebe\eds\workstream\20260919_160000_V20260919_1600_core_engine_plpgsql.sql`  
- Version File: `C:\Users\edebe\eds\TradeApps\breakout\fs\constants.py`  

---

## Check List of Changes

- [ ] **Task 1: Workstream Initialization & Version Bump**
  - [x] Create task lifecycle file.
  - [ ] Bump version in `TradeApps/breakout/fs/constants.py` to `V20260919_1600`.
- [ ] **Task 2: Step 1 - Leaf Helpers Translation**
  - [ ] `sp_helper_is_sim_db`
  - [ ] `sp_helper_check_alt_net_return`
  - [ ] `sp_9004_SetTrailingStopLossOnProfit`
  - [ ] `sp_9002_CheckTradeSignalForClosure`
  - [ ] `usp_cleanup_stale_open_trades`
  - [ ] Compile and test in PostgreSQL `tradedb`.
- [ ] **Task 3: Step 2 - Core Pricing, Exits & Entry Engine**
  - [ ] `sp_002_UpdateCombinedTradesOpen`
  - [ ] `sp_003_CloseTradesTargetReached_refactored`
  - [ ] `sp_001_create_trades_brk`
  - [ ] Compile and test in PostgreSQL `tradedb`.
- [ ] **Task 4: Step 3 - Supervisor Procedure**
  - [ ] `sp_loop_create_trades_v2`
  - [ ] Test single-iteration execution in PostgreSQL `tradedb`.
- [ ] **Task 5: Lifecycle Completion**
  - [ ] Move task file to `workstream/300_complete/`.
  - [ ] Present validation report with check boxes.

---

## Implementation Log
- **2026-09-19 16:00:00** - Workstream task initialized in `workstream/200_inprogress/`.
