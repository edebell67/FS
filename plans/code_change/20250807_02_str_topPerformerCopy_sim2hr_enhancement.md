# Gemini Coder - Plan for 02_str_topPerformerCopy_sim2hr.py Enhancement

This document outlines the purpose and recent enhancements to `02_str_topPerformerCopy_sim2hr.py`.

## 1. Purpose

`02_str_topPerformerCopy_sim2hr.py` is an automated trade execution script designed for simulated trading, specifically utilizing model performance data aggregated over a 2-hour period. It identifies the best-performing model and signal based on this 2-hour data and executes trades if no active, tradeable trade for the same model and signal (originating from this script) already exists.

## 2. Implemented Changes

*   **`algo_viewer/strategy_library/02_str_topPerformerCopy_sim2hr.py`**:
    *   **API Endpoint**: Uses `http://127.0.0.1:8000/api/vw_106_ModelPerformance_alt_2hr` for model performance data.
    *   **`has_open_trade` Function Enhancement (2025-08-07)**: The `has_open_trade` function was updated to include a check for `t.get('reason') == SCRIPT_NAME`. This ensures that when checking for existing open trades, only those trades that originated from this specific script are considered. This prevents interference from other strategies that might target the same model/signal.

## 3. Verification

*   The script should continue to interact with the simulated database (`tradedb_sim`) and fetch 2-hour aggregated model performance data.
*   The `has_open_trade` function should now correctly identify existing trades that originated from `02_str_topPerformerCopy_sim2hr.py`.
*   The script should prevent duplicate trades for the same model/signal pair if an active trade from this script already exists.
