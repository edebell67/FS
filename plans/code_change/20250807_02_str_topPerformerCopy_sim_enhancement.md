# Gemini Coder - Plan for 02_str_topPerformerCopy_sim.py Enhancement

This document outlines the purpose and recent enhancements to `02_str_topPerformerCopy_sim.py`.

## 1. Purpose

`02_str_topPerformerCopy_sim.py` is an automated trade execution script designed for simulated trading. It identifies the best-performing model and signal and executes trades if no active, tradeable trade for the same model and signal (originating from this script) already exists. It uses a cleaner approach for handling API parameters and interacts with a simulated database (`tradedb_sim`).

## 2. Implemented Changes

*   **`algo_viewer/strategy_library/02_str_topPerformerCopy_sim.py`**:
    *   **API Parameter Handling**: Uses a `params` dictionary in `fetch_data` for cleaner URL query parameter construction.
    *   **`has_open_trade` Function Enhancement (2025-08-07)**: The `has_open_trade` function was updated to include a check for `t.get('reason') == SCRIPT_NAME`. This ensures that when checking for existing open trades, only those trades that originated from this specific script are considered. This prevents interference from other strategies that might target the same model/signal.

## 3. Verification

*   The script should continue to interact with the simulated database (`tradedb_sim`).
*   The `has_open_trade` function should now correctly identify existing trades that originated from `02_str_topPerformerCopy_sim.py`.
*   The script should prevent duplicate trades for the same model/signal pair if an active trade from this script already exists.
