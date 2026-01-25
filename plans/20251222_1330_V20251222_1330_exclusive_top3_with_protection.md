# 20251222_1330_V20251222_1330_Exclusive_Top3_With_Protection

## 1. Understanding of Requirements
The user wants to refine the "Top 3" auto-activation logic to make it exclusive and dynamic while protecting strategies that have open live trades.

The new logic is:
1.  A currently active strategy with at least one open "L" (Live) trade is **protected** and must remain active.
2.  The system should then fill the remaining slots in the "Top 3" with the best-performing (by trade count) inactive strategies.
3.  Any previously active strategy that is *not* protected and does not make it into the new Top 3 should be **deactivated**.

**Example:**
*   `Strategy A` is active and has an open L trade (Protected).
*   `Strategy B` is active but has no open L trades.
*   The system will keep `Strategy A` active. It now has 2 slots to fill.
*   It finds that `Strategy C` and `Strategy D` are the top 2 profitable, inactive strategies.
*   The end result is: `A`, `C`, and `D` are active. `B` is deactivated.

## 2. Plan of Approach
1.  **Modify `_perform_auto_activation_check` in `TradeApps/breakout/common.py`**:
    *   This function needs a way to identify which strategies have open live trades. It currently scans closed trades. I will add a scan for **open** trades.
    *   I'll create a set of `protected_keys` by scanning today's open trade files and identifying which active strategies own them.
    *   I'll count the number of protected keys to determine how many new strategies can be activated (`slots_to_fill = 3 - len(protected_keys)`).
    *   The existing activation logic will be modified to only pick the top `slots_to_fill` candidates.
    *   The deactivation logic will be expanded: a strategy will now be deactivated if its master switch is off OR if it's not in the new `final_active_set` (which includes protected keys + new top candidates).

## 3. List of Changes

### `TradeApps/breakout/common.py`
- [ ] Update `_perform_auto_activation_check` function:
    - [ ] **Identify Protected Keys**:
        - Before any other logic, scan open trade files for the day.
        - Create a `protected_keys` set containing the activation keys of any active strategy that has an open live trade.
    - [ ] **Calculate Slots**: Determine `slots_to_fill = 3 - len(protected_keys)`.
    - [ ] **Activation Logic**:
        - In the candidate selection, fetch the top `slots_to_fill` profitable, inactive strategies (instead of a fixed 3).
    - [ ] **Deactivation Logic**:
        - Create a `final_active_set` = `protected_keys` + `newly_activated_keys`.
        - Iterate through all of the process's owned keys in `activations.json`.
        - Deactivate any key if its master switch is off, OR if it's not in the `final_active_set`.

### `TradeApps/breakout/constants.py`
- [ ] Update `VERSION` to `V20251222_1330`.

## 4. Verification Plan
- [ ] Create mock JSON files simulating the scenario in the requirements.
- [ ] Verify that the protected strategy remains active, the non-protected active one is deactivated, and the top new strategies are activated correctly.
