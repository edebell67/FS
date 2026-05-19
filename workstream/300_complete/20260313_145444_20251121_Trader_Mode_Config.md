# Plan: Configurable Trader Mode (LIVE/SIM)

**Date:** 2025-11-21

This document outlines the plan to implement a configurable "Trader Mode" that allows the `simple_trend_trader.py` script to switch between LIVE and SIM data sources. The mode will be controlled via the `trade_monitor.py` application.

### 1. Understanding of Requirements

The goal is to make the data source for the `simple_trend_trader.py` script configurable, allowing it to switch between a "LIVE" and a "SIM" API endpoint. The selection of which endpoint to use will be controlled by a new `trader_mode` setting in a configuration file, and this setting will be manageable from the `trade_monitor.py` UI.

**Core Requirements:**

1.  **Create a Configuration File:**
    *   A new JSON file (`config.json`) will be created to store the `trader_mode`.
    *   This file will be read by both `simple_trend_trader.py` and `trade_monitor.py`.
    *   The `trader_mode` can be either "LIVE" (default) or "SIM".

2.  **Modify `simple_trend_trader.py`:**
    *   This script needs to read the `config.json` file on startup.
    *   Based on the `trader_mode`, it will set its `API_URL` to one of two values:
        *   **LIVE**: `http://127.0.0.1:8000/api/vw_000_fx_quotes?db=tradedb`
        *   **SIM**: `http://127.0.0.1:8000/api/vw_000_fx_quotes?db=tradedb_sim2`

3.  **Enhance `trade_monitor.py`:**
    *   A new UI page or a new option within an existing page is needed to manage the `trader_mode`.
    *   The user should be able to see the current mode and switch it between "LIVE" and "SIM".
    *   This change must be saved back to the `config.json` file. The "Configure Real-Time (RT) Trades" page is the most logical place for this new setting.

### 2. Detailed Implementation Checklist

**Phase 1: Configuration Management**

*   [ ] **1.1. Create Config Helper Functions:**
    *   In `trade_monitor.py`, create a new set of helper functions to manage `config.json`.
    *   `_get_main_config_path()`: Will define the path to a new `config.json` file.
    *   `load_main_config()`: Will read `config.json` and return the configuration dictionary. It will create a default file with `{"trader_mode": "LIVE"}` if one doesn't exist.
    *   `save_main_config(config_data)`: Will write a dictionary to `config.json`.
*   [ ] **1.2. Re-use Config Logic:**
    *   Copy these same helper functions into `simple_trend_trader.py` so both scripts can read and write to the same configuration file.

**Phase 2: Update `simple_trend_trader.py`**

*   [ ] **2.1. Integrate Config Loading:**
    *   At the start of the script, call `load_main_config()` to get the current `trader_mode`.
*   [ ] **2.2. Implement Dynamic API URL:**
    *   Modify the `API_URL` definition. Instead of being a single constant, it will be set dynamically based on the `trader_mode` read from the config.

**Phase 3: Update `trade_monitor.py` UI**

*   [ ] **3.1. Add Trader Mode to "Configure RT Trades" Page:**
    *   Modify the `view_rt_trade_selector` function.
    *   At the top of the page, before the list of trade titles, it will display the "Current Trader Mode".
    *   The prompt at the bottom will be updated to include a new option, e.g., `'m' to toggle mode`.
*   [ ] **3.2. Implement Mode Toggling Logic:**
    *   In the input handling loop of `view_rt_trade_selector`, add an `elif` block for the new 'm' choice.
    *   When the user enters 'm', the script will:
        1.  Load the current config using `load_main_config()`.
        2.  Flip the `trader_mode` from "LIVE" to "SIM", or from "SIM" to "LIVE".
        3.  Save the updated configuration back to the file using `save_main_config()`.
        4.  The page will then auto-refresh, displaying the newly set mode.
