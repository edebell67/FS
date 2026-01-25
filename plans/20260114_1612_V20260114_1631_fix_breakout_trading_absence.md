# Fix Breakout Trading Absence

Explain why trades are not being generated and provide a plan to restore regular breakout trading.

## Analysis of the Issue

My investigation has revealed three primary reasons why `breakout.py` is not generating trades:

1.  **Logic Bypass Enabled**: In `config.json`, the setting `"bypass_criteria_check": true` is active. This global flag causes `BaseBreakoutStrategy` to skip its standard `check_and_enter` logic (where the breakout rules are defined) and instead attempt a "bypass entry" based solely on whether a strategy is pre-activated and passing a profit guard.
2.  **Activation Name Mismatch**: The bypass entry logic relies on the strategy being "active" in `activations.json`. However, `activations.json` currently only contains entries for strategies with the `breakout_R_Rev` alias. `breakout.py` uses the alias `breakout`. Since no `breakout_` keys exist (or they are set to `active: false`), the strategy is never considered active.
3.  **Zero-History Probation (ZHP)**: The profitability guard in `common.py` implemented a "Zero-History Probation" (ZHP) check. If a strategy has no historical trades on disk, it is automatically blocked. This prevents new strategy configurations from ever getting their first trade unless seeded manually.

## Proposed Changes

### [Configuration]

#### [MODIFY] [config.json](file:///C:/Users/edebe/eds/TradeApps/breakout/config.json)

*   Change `"bypass_criteria_check": true` to `"bypass_criteria_check": false`. This will restore the execution of the breakout logic defined in `breakout.py`.

### [Environment]

#### [MODIFY] [activations.json](file:///C:/Users/edebe/eds/TradeApps/breakout/activations.json)

*   (Optional but recommended) Ensure the `breakout` alias is recognized or that the user activates the desired breakout parameters. However, with `bypass_criteria_check` set to `false`, the strategy will at least *attempt* to enter based on price logic, though it may still be blocked at the order stage if not activated.

### [Core Logic]

#### [MODIFY] [common.py](file:///C:/Users/edebe/eds/TradeApps/breakout/common.py)

*   Consider relaxing the ZHP (Zero-History Probation) to allow new strategies to trade if no history is found, or if they are explicitly manually activated.

#### [MODIFY] [constants.py](file:///C:/Users/edebe/eds/TradeApps/breakout/constants.py)

*   Update `VERSION` to `V20260114_1631`.

## Verification Plan

### Automated Tests
*   Run `python test_breakout_logic.py`. This test currently fails because of the global `bypass_criteria_check`. After setting it to `false`, this test should pass, proving the breakout logic is being correctly triggered by price ticks.

### Manual Verification
*   Monitor the console output of `breakout.py` to ensure it is printing price updates and "Building window" messages.
*   Verify that when a breakout occurs, the "NEW TRADE" message appears in the logs.
