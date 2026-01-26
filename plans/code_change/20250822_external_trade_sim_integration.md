# Gemini Coder - Plan for External Trade Execution Simulation Integration

## 1. Understanding of Requirements

The goal is to introduce a "simulation" version of the external trade execution utility (`trade_execution_utils.py`) that directs trade execution commands to a simulation database endpoint. The `tradepanel/trade_engine.py` will then conditionally use either the live or simulation version of this utility based on its `is_simulation_mode` flag. The internal trade management process will remain unaffected by the success or failure of the external execution.

## 2. Plan of Approach

1.  **Add New Constant**: Define a new constant in `tradepanel/constants.py` for the simulation external trade execution endpoint.
2.  **Create Simulation Utility File**: Create a new Python file (`trade_execution_utils_sim.py`) in `algo_viewer/common_utils/`. This file will be a copy of the original `trade_execution_utils.py` but modified to target the simulation endpoint and pass the `db` parameter.
3.  **Conditional Import in Trade Engine**: Modify `tradepanel/trade_engine.py` to conditionally import and use the appropriate external trade execution function (live or sim) based on the `TradeManager`'s `is_simulation_mode` attribute.

## 3. List of Changes

*   **`tradepanel/constants.py`**:
    *   [x] Add `EXTERNAL_TRADE_EXECUTION_ENDPOINT_SIM: Final[str] = f"{API_BASE_URL}/execute_trade_sim/"` (using `API_BASE_URL` for consistency).

*   **`C:\Users\edebe\eds\algo_viewer\common_utils\trade_execution_utils_sim.py`**:
    *   [x] Create this new file.
    *   [x] Copy the content of `trade_execution_utils.py` into it.
    *   [x] Add `from tradepanel import constants` at the top.
    *   [x] Modify the `execute_trade_reusable` function:
        *   Change `execute_trade_endpoint` to `constants.EXTERNAL_TRADE_EXECUTION_ENDPOINT_SIM`.
        *   Add `params={"db": constants.SIM_DB_SUFFIX.split('=')[1]}` to the `requests.post` call to ensure the simulation database is targeted.

*   **`tradepanel/trade_engine.py`**:
    *   [x] Modify the import of `execute_trade_reusable`:
        *   Change `from algo_viewer.common_utils.trade_execution_utils import execute_trade_reusable` to:
            ```python
            from algo_viewer.common_utils.trade_execution_utils import execute_trade_reusable as live_execute_trade_reusable
            from algo_viewer.common_utils.trade_execution_utils_sim import execute_trade_reusable as sim_execute_trade_reusable
            ```
    *   [x] Modify `TradeManager.__init__`:
        *   Add conditional assignment for the external trade executor function:
            ```python
            if self.is_simulation_mode:
                self._external_trade_executor = sim_execute_trade_reusable
                logger_trade_manager.info("TradeManager initialized in SIMULATION mode. Using sim_execute_trade_reusable.")
            else:
                self._external_trade_executor = live_execute_trade_reusable
                logger_trade_manager.info("TradeManager initialized in LIVE mode. Using live_execute_trade_reusable.")
            ```
    *   [x] Update calls to `execute_trade_reusable` in `execute_automated_buy_trade` and `execute_automated_sell_trade` to use `self._external_trade_executor`.

## 4. Verification

*   Confirm that `tradepanel/constants.py` contains the new `EXTERNAL_TRADE_EXECUTION_ENDPOINT_SIM`.
*   Confirm that `algo_viewer/common_utils/trade_execution_utils_sim.py` exists and its `execute_trade_reusable` function correctly targets the simulation endpoint with the `db` parameter.
*   Confirm that `tradepanel/trade_engine.py` conditionally imports and uses the correct external trade execution function based on `is_simulation_mode`.
*   Run the application in both live and simulation modes to ensure external trade execution calls are made to the correct endpoints.
