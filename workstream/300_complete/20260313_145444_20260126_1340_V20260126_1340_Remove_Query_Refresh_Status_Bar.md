# Plan: Remove Query Refresh Status Bar [V20260126_1340]

This plan removes the "Query Refresh Status Bar" (loading overlay) from the standard Multi-Chart dashboard as requested by the user.

## 1. Requirements
*   **Remove UI Overlay**: Delete the `loadingOverlay` div and its associated styles from `multi_chart.html`.
*   **Remove JS Logic**: Delete `showLoader`, `hideLoader`, and their calls from `multi_chart.js` to prevent script errors.

## 2. Plan of Approach

### A. HTML/CSS Cleanup (`multi_chart.html`)
*   Remove the `<div id="loadingOverlay">` block.
*   Remove the `.loading-overlay` and `.loader-bar` CSS definitions.

### B. JavaScript Cleanup (`multi_chart.js`)
*   Delete the `showLoader` and `hideLoader` functions.
*   Remove the `showLoader` and `hideLoader` calls within the `fetchData` function.

### C. Versioning
*   Update version to `V20260126_1340`.

## 3. Checklist
*   [ ] `multi_chart.html`: CSS for loader removed.
*   [ ] `multi_chart.html`: HTML for loader removed.
*   [ ] `multi_chart.js`: `showLoader`/`hideLoader` functions removed.
*   [ ] `multi_chart.js`: calls in `fetchData` removed.
*   [ ] `constants.py`: Version updated to `V20260126_1340`.

## 4. Verification
*   Open standard dashboard.
*   Click "Refresh".
*   Confirm data syncs silently in the background without the blue status bar popping up.
