# Live and Simulation Mode Separation Plan

## 1. Objective

The primary objective is to enable a clear and robust separation between "live" and "simulation" modes for the trading application. This separation must encompass:
1.  **Participant Trading Data:** Ensuring that open positions, cash, realized P/L, trade history, and other participant-specific data generated in live mode do not interfere with data generated in simulation mode, and vice-versa.
2.  **Market Price Feed:** Allowing the application to fetch prices from a "live" external source or a "simulation" external source (e.g., a different database or API endpoint) based on the active mode.

This separation will be controlled by a single configuration flag, making it easy to switch between modes.

## 2. Current State Analysis

*   **Data Persistence:** All participant states, market data, and logs are currently stored within a single `DATA_DIR` (defined in `config.py` as `simulation_data`). This means live and simulation runs would overwrite each other's data.
*   **Price Feed:** The `PRICE_FEED_URL` is a single, hardcoded entry in `config.py`. `market_simulator.py` uses this URL to fetch prices. There is no mechanism to conditionally switch the price feed URL based on a mode.
*   **Mode Flag:** There is no explicit "simulation mode" flag that governs the entire Python application's behavior.

## 3. Revised Plan of Approach

The plan involves introducing a master `IS_SIMULATION_MODE` flag and making data directory paths and price feed URLs dynamic based on this flag.

### 3.1. Data Separation Strategy

To separate participant trading data, we will introduce distinct base data directories for live and simulation modes. The `DATA_DIR` variable in `config.py` will then be dynamically set based on the `IS_SIMULATION_MODE` flag. This ensures all data persistence operations (saving/loading participant states, market data, logs) automatically use the correct, isolated directory.

### 3.2. Price Feed Separation Strategy

To separate price feeds, we will define two distinct price feed URLs in `config.py`: one for live and one for simulation. The `fetch_external_price` function in `market_simulator.py` will then select the appropriate URL based on the `IS_SIMULATION_MODE` flag.

## 4. Detailed List of Changes

### 4.1. `Game_trader/config.py`

*   **Remove:**
    ```python
    DATA_DIR = 'simulation_data'
    # ... and all paths derived from DATA_DIR (MARKET_DATA_FILE, PARTICIPANTS_DIR, etc.)
    PRICE_FEED_URL = 'http://127.0.0.1:8000/api/vw_000_fx_quotes'
    ```

*   **Add/Modify:**
    ```python
    # --- Mode Configuration ---
    IS_SIMULATION_MODE = False # Set to True for simulation mode, False for live mode

    # --- Data Persistence Configuration (Dynamic) ---
    LIVE_DATA_DIR = 'live_data'
    SIM_DATA_DIR = 'simulation_data'

    DATA_DIR = SIM_DATA_DIR if IS_SIMULATION_MODE else LIVE_DATA_DIR

    MARKET_DATA_FILE = os.path.join(DATA_DIR, 'market_data.json')
    PARTICIPANTS_DIR = os.path.join(DATA_DIR, 'participants')
    MAIN_LOG_FILE = os.path.join(DATA_DIR, 'simulation_log.jsonl')
    EXPERT_DATA_FILE = os.path.join(DATA_DIR, 'expert_data.jsonl')

    # --- External Price Feed Configuration (Dynamic) ---
    LIVE_PRICE_FEED_URL = 'http://127.0.0.1:8000/api/vw_000_fx_quotes'
    SIM_PRICE_FEED_URL = 'http://127.0.0.1:8000/api/vw_000_fx_quotes?db=tradedb_sim2'

    # The actual URL used will be selected in market_simulator.py based on IS_SIMULATION_MODE
    ```

### 4.2. `Game_trader/data_persistence.py`

*   **No direct changes needed.** This file already imports `DATA_DIR`, `MARKET_DATA_FILE`, `PARTICIPANTS_DIR`, etc., from `config.py`. These variables will now be dynamically set in `config.py` based on the `IS_SIMULATION_MODE` flag, ensuring all data operations automatically target the correct directory.

### 4.3. `Game_trader/market_simulator.py`

*   **Update Imports:**
    *   Modify the import statement for configuration variables to include `LIVE_PRICE_FEED_URL`, `SIM_PRICE_FEED_URL`, and `IS_SIMULATION_MODE`.
    *   Remove `PRICE_FEED_URL` from imports.

*   **Modify `fetch_external_price` function:**
    *   Inside this function, select the appropriate price feed URL based on `IS_SIMULATION_MODE`.

    ```python
    # ... (existing imports) ...
    from config import (
        # ... other imports ...
        LIVE_PRICE_FEED_URL,
        SIM_PRICE_FEED_URL,
        IS_SIMULATION_MODE,
    )

    def fetch_external_price():
        if not USE_EXTERNAL_PRICE_FEED:
            return None

        # Select the effective price feed URL based on the simulation mode
        effective_price_feed_url = SIM_PRICE_FEED_URL if IS_SIMULATION_MODE else LIVE_PRICE_FEED_URL

        try:
            response = requests.get(effective_price_feed_url, timeout=PRICE_FEED_TIMEOUT_SECONDS)
            # ... rest of the function logic remains the same ...
        except Exception as exc:
            # ... (existing error handling) ...
    ```

### 4.4. `Game_trader/trader_game.py`

*   **Update Imports:**
    *   Modify the import statement for configuration variables to include `IS_SIMULATION_MODE`.

*   **Modify `simulation_state` dictionary:**
    *   Add `IS_SIMULATION_MODE` to the `simulation_state` dictionary so its status is globally accessible within the application.

    ```python
    # ... (existing global variables) ...
    from config import INITIAL_GBP_USD, SPREAD, PRICE_UPDATE_INTERVAL_SECONDS, RL_AGENT_IDS, NUMBER_OF_RULE_BASED_PARTICIPANTS, IS_SIMULATION_MODE # Add IS_SIMULATION_MODE

    # ... (existing simulation_state definition) ...
    simulation_state = {
        # ... (existing entries) ...
        'IS_SIMULATION_MODE': IS_SIMULATION_MODE, # Add this line
        # ... (existing entries) ...
    }
    ```

## 5. Verification

After implementing these changes, verification will involve:
1.  **Running in Live Mode:** Set `IS_SIMULATION_MODE = False` in `config.py`. Start the application and confirm that it uses the `live_data` directory for persistence and fetches prices from `LIVE_PRICE_FEED_URL`.
2.  **Running in Simulation Mode:** Set `IS_SIMULATION_MODE = True` in `config.py`. Start the application and confirm that it uses the `simulation_data` directory for persistence and fetches prices from `SIM_PRICE_FEED_URL`.
3.  **Data Integrity:** Ensure that data generated in one mode does not appear in the other mode's directories.

This plan provides a clear, configurable, and robust solution for separating live and simulation environments.

## 6. Feature: Front-end Checkbox for Simulation Mode

**Objective:** To allow users to dynamically switch between live and simulation price feeds via a front-end checkbox without requiring an application restart for the price feed change.

**Limitation:** Changing the `IS_SIMULATION_MODE` via the front-end checkbox will *only* affect the price feed URL. The data persistence location (i.e., whether data is saved to `live_data/` or `simulation_data/`) is determined at application startup based on the `IS_SIMULATION_MODE` value in `config.py`. To switch the data persistence location, a **full application restart is required** after changing `IS_SIMULATION_MODE` in `config.py`.

### Tasks Checklist:

*   **Backend (`Game_trader/trader_game.py`)**
    *   [x] **Refactor `IS_SIMULATION_MODE`:** Ensure `IS_SIMULATION_MODE` is a mutable global variable within `trader_game.py` (or part of `simulation_state`) that can be modified at runtime.
    *   [x] **New API Endpoint:** Add `@app.route('/admin/set_simulation_mode', methods=['POST'])` to handle requests from the front-end.
    *   [x] **Update `simulation_state`:** The new API endpoint will update `simulation_state['IS_SIMULATION_MODE']` based on the received value.
    *   [x] **Update `get_game_status`:** Ensure the `/game/status` endpoint returns the current `simulation_state['IS_SIMULATION_MODE']` so the front-end can initialize the checkbox correctly.

*   **Backend (`Game_trader/market_simulator.py`)**
    *   [x] **Access from `global_state`:** Modify `fetch_external_price` to retrieve the `IS_SIMULATION_MODE` value from the `global_state` dictionary (which is `simulation_state`) passed to `update_market_prices`, instead of directly from `config.py`.
    *   [x] **Remove direct `config` import:** Remove `IS_SIMULATION_MODE` from the direct import from `config.py` in `market_simulator.py`.

*   **Frontend (`Game_trader/trading_activity_viewer_frontend.html`)**
    *   [x] **Add Checkbox:** Insert an HTML checkbox element (e.g., `<input type="checkbox" id="simModeToggle">`) in the admin controls section.
    *   [x] **Add Label:** Add a corresponding label (e.g., "Enable Simulation Mode").
    *   [x] **JavaScript - Initial State:** On page load, fetch the current `IS_SIMULATION_MODE` from the `/game/status` API endpoint and set the checkbox's `checked` state accordingly.
    *   [x] **JavaScript - Event Listener:** Add an event listener to the checkbox. When its state changes:
        *   Send an AJAX POST request to the new `/admin/set_simulation_mode` endpoint with the new boolean value (`true` or `false`).
        *   Display a user-friendly message (e.g., using `alert()` or updating a status div) confirming the change and reiterating the limitation: "Simulation mode for price feed updated. Note: Changing data persistence (live_data/simulation_data) requires application restart."

*   **`Game_trader/config.py`**
    *   [x] **Adjust `IS_SIMULATION_MODE` import:** Ensure `trader_game.py` imports `IS_SIMULATION_MODE` from `config.py` for its *initial* value, but then manages it in `simulation_state`. (This is already done from the previous step, but worth noting for clarity).
