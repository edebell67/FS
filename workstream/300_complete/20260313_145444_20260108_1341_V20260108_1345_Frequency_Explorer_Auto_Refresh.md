# Plan for Adding Auto Refresh to Frequency Explorer (2026-01-08)

## 1. Understanding of Requirements
The user wants to add an "Auto Refresh" feature to the Frequency Explorer screen. Currently, the screen has a manual "Update" button. The JavaScript code already has some skeleton logic for auto-refresh (pointing to a missing checkbox with ID `autoRefreshCheck`), but the UI element itself is missing from the HTML.

## 2. Plan of Approach
1.  **Add UI Element**: Insert a checkbox for "Auto Refresh" in the `.controls` section of `frequency_explorer.html`.
2.  **Enhance Logic**:
    *   Initialize the `refreshTimer` if the checkbox is checked on load.
    *   Update `toggleAutoRefresh` to handle starting/stopping the interval.
    *   Ensure the "Update" button still works manually.
    *   Add comments with the next version number and timestamp.
3.  **Version Update**:
    *   Update `constants.py` with the new version number `V20260108_1345`.
    *   Update the sidebar version in `frequency_explorer.html` to `v2026.01.08.1345`.
4.  **Verification**: Confirm that checking/unchecking the box starts/stops the timer and that data is fetched successfully.

## 3. Check List of Changes
*   [x] Modify `TradeApps/breakout/frequency_explorer.html`:
    *   [x] Add the "Auto Refresh" checkbox and label to the controls area.
    *   [x] Update the version string in the sidebar.
    *   [x] Add comments to changes with `V20260108_1345`.
*   [x] Modify `TradeApps/breakout/constants.py`:
    *   [x] Update `VERSION` to `V20260108_1345`.

## 4. Confirmation Plan
*   Verify the "Auto Refresh" checkbox appears on the Frequency Explorer page.
*   Verify that when checked, the "Last update" timestamp updates every 30 seconds.
*   Verify that unchecking stops the auto-update.
*   Verify the version string in the sidebar matches the new version.
