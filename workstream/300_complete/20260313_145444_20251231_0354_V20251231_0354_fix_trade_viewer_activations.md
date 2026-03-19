# Plan: Fix Trade Activation and Mode Segmentation in Trade Viewer

This document outlines the plan to synchronize `trade_viewer.html` with the new mode-segmented `activations.json` structure and ensure proper activation key building.

## 1. Understanding of Requirements

*   `activations.json` has changed from a flat dictionary to a mode-segmented structure (`{"live": {...}, "sim": {...}}`).
*   Activation keys now include the strategy parameters (e.g., `breakout_R_Rev_2_tp3.0_sl6.0_2_0.00015_3.0_6.0_sell_net`).
*   `trade_viewer.html` is currently building keys without parameters and fetching activations without specifying the mode.

## 2. Plan of Approach

1.  **Read and Update `trade_viewer.html`**:
    *   Initialize a global `activeRunMode` variable.
    *   Update `loadConfig` to set `activeRunMode` from the configuration.
    *   Update `loadActivations` to:
        *   Accept an optional `mode` parameter.
        *   Pass `?mode=${mode}` to the `/api/activations` endpoint.
    *   Update `buildActivationKey` to include strategy parameters in the key.
    *   Update `renderSummary` to:
        *   Pass the strategy parameters when calling `buildActivationKey`.
        *   Pass the current `activeRunMode` when performing auto-activations (POST to API).
    *   Update `toggleActivation` to:
        *   Accept the strategy parameters.
        *   Pass the current `activeRunMode` in the POST body.

## 3. List of Changes

### `trade_viewer.html`

*   [ ] Initialize `let activeRunMode = 'live';` in the global scope.
*   [ ] Update `loadConfig()`:
    ```javascript
    async function loadConfig() {
        // ...
        if (data.success) {
            currentConfig = data.config;
            activeRunMode = currentConfig.run_mode || 'live';
            document.getElementById('runMode').value = activeRunMode;
            loadActivations(); // Reload activations for the correct mode
        }
    }
    ```
*   [ ] Update `loadActivations()`:
    ```javascript
    async function loadActivations() {
        const mode = activeRunMode;
        const response = await fetch(`/api/activations?mode=${mode}`);
        // ... rest stays same but ensure it handles the response ...
    }
    ```
*   [ ] Update `buildActivationKey(appName, strategy, direction, type)`:
    ```javascript
    function buildActivationKey(appName, strategy, direction, type) {
        if (strategy && strategy !== '-') {
            return `${appName}_${strategy}_${direction}_${type}`;
        }
        return `${appName}_${direction}_${type}`;
    }
    ```
*   [ ] Update `renderSummary(groupedData)`:
    *   Update all calls to `buildActivationKey` to include `group.strategy`.
    *   Update the auto-activation `fetch` to include `mode: activeRunMode` in the body.
*   [ ] Update `toggleActivation(appName, strategy, product, direction, type, sourceEl)`:
    *   Include `strategy` in arguments.
    *   Pass `mode: activeRunMode` in the POST body.
*   [ ] Update `renderStatusRow` and individual card rendering to correctly determine activation status using the new keys.

## 4. Verification

*   Open Trade Viewer.
*   Verify that "Net" and "Alt" checkboxes reflect the state in `activations.json` for the current mode.
*   Toggle a checkbox and verify it saves to the correct mode and with the correct key (including params) in `activations.json`.
