# Gemini Coder - Plan for 03_str_topPerformerAtPriceSpread_sim.py Function

This document outlines the function and key characteristics of the new simulation strategy script: `03_str_topPerformerAtPriceSpread_sim.py`.

## 1. Purpose

`03_str_topPerformerAtPriceSpread_sim.py` is a new automated trade execution script designed for **simulated trading**. It combines the robust simulation environment setup from `02_str_topPerformerCopy_sim.py` with advanced trade entry criteria based on `alt_net_return` and the consideration of multiple top-performing models.

Its primary function is to:
*   Identify the top `TOP_N_MODELS` (configurable, default 3) based on their `total_return` from the model performance API.
*   For each of these top model/signal pairs, check if there exists *any* open trade with an `alt_net_return` value less than a predefined threshold (`ALT_NET_RETURN_THRESHOLD`, default -100).
*   If this condition is met, execute a simulated trade.

## 2. Key Characteristics and Integrated Logic

*   **Base Script**: Built upon `02_str_topPerformerCopy_sim.py`, inheriting its structure for API interaction, logging, and simulation-specific trade execution (`execute_trade_sim`).
*   **Configuration**: Includes new constants `ALT_NET_RETURN_THRESHOLD` and `TOP_N_MODELS` for flexible strategy tuning.
*   **Model Selection**: Utilizes a modified `get_top_n_signals_and_prices` function (renamed from `get_best_signal_and_price`) to retrieve a list of the top N models based on `total_return`.
*   **Trade Entry Criteria**: The core trade triggering logic is based on the `alt_net_return` of existing open trades for a given model/signal. If any such trade has an `alt_net_return` below `ALT_NET_RETURN_THRESHOLD`, a new trade is initiated.
*   **Open Trade Check (`has_open_trade`)**: The `has_open_trade` function ensures that a new trade is not opened if an active, tradeable trade for the same model and signal *and originating from this specific script* already exists. This is achieved by checking `t.get('reason') == SCRIPT_NAME`.
*   **Trade Reason**: Simulated trades executed by this script will have their `reason` attribute set to the script's filename (`SCRIPT_NAME`).
*   **Logging**: Provides detailed logging for each cycle, including evaluation of top models, open trade checks, and trade execution outcomes.

## 3. Verification Points

*   Confirm that the script correctly identifies and processes the top N models based on `total_return`.
*   Verify that simulated trades are only placed when the `alt_net_return` condition is met for an existing open trade.
*   Ensure that the `has_open_trade` function correctly prevents duplicate trades from this script.
*   Check that the `reason` for executed simulated trades is correctly set to `03_str_topPerformerAtPriceSpread_sim` in the logs and database.
*   Monitor `03_str_topPerformerAtPriceSpread_sim.log` for expected behavior and any errors.
