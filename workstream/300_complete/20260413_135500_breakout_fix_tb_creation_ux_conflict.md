# Task: Fix UX Conflict in 'Create Trade Bucket' and 'Trade Drilldown'

## 1. Understanding of Requirements
The user reports that selecting the "Create Trade Bucket" button results in seeing trade breakdown details (the Drilldown modal) instead of creating/opening a bucket. This suggests a conflict between button click events and the card's double-click event, or a misconfigured button action.

## 2. Plan of Approach
1.  **Isolate Click Events**: In `multi_chart.js`, ensure that button clicks inside the `.chart-actions` container stop event propagation to prevent triggering any card-level event listeners (like double-click).
2.  **Verify Button Actions**:
    *   Double-check that the `action-btn.save` button is correctly calling `saveToBucket(groupName)`.
    *   Confirm that `saveToBucket` is successfully hitting the API and not throwing a silent error that keeps the user on the current page.
3.  **UI/UX Improvement**:
    *   Change the icon for `saveToBucket` to something distinct (e.g., `fa-save` or `fa-folder-plus`) to differentiate it from "Add All Windows".
    *   Add `event.stopPropagation()` to all action buttons in the card header.

## 3. List of Changes
*   **`TradeApps/breakout/fs/multi_chart.js`**:
    *   [ ] Update `createGroupCard` template to include `event.stopPropagation()` on button clicks.
    *   [ ] Change the "Save to Bucket" icon to `fa-folder-plus`.
    *   [ ] Add logging to `saveToBucket` to confirm execution flow.
*   **`TradeApps/breakout/fs/constants.py`**:
    *   [ ] Update version to `V20260413_1355`.
