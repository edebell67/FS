# Plan: Sidebar Navigation and Activations Explorer UI

This document outlines the plan to implement a global sidebar navigation menu and a new dedicated Activations Explorer page.

## 1. Requirements
*   Create a new `activations_explorer.html` page to manage `activations.json`.
*   Implement a sidebar menu on the left side of every page.
*   The sidebar should replace existing navigation links in headers.
*   The sidebar must be visible on all pages.
*   Ensure the UI is sleek and consistent with the existing theme.

## 2. Approach
1.  **Sidebar CSS**: Create a shared `sidebar.css` file to define the sidebar layout (width, colors, hover states).
2.  **Sidebar HTML Template**: Define a standard HTML snippet for the sidebar.
3.  **Refactor Existing Pages**:
    *   Inject the sidebar HTML.
    *   Include `sidebar.css`.
    *   Adjust the main `.container` or create a `.main-content` wrapper to have a `margin-left` for the sidebar.
    *   Remove legacy header links.
4.  **`activations_explorer.html`**:
    *   Build a new page from scratch using the sidebar.
    *   Fetch data from `/api/activations`.
    *   Display strategies as rows with columns for Net/Alt Buy/Sell and checkboxes/switches for assigned products.
    *   Incorporate search/filtering by strategy name or product.

## 3. List of Changes
*   **`constants.py`**:
    *   [x] Update `VERSION` to `V20260102_0145`.
*   **`sidebar.css`**:
    *   [x] Create new file with glassmorphic sidebar styles.
*   **`activations_explorer.html`**:
    *   [x] Create new file for activations management.
*   **`trade_viewer.html`**:
    *   [x] Add sidebar HTML.
    *   [x] Reference `sidebar.css`.
    *   [x] Adjust layout for sidebar.
    *   [x] Remove old navigation links.
*   **`strategy_performance.html`**:
    *   [x] Add sidebar HTML.
    *   [x] Reference `sidebar.css`.
    *   [x] Adjust layout for sidebar.
    *   [x] Remove old navigation links.
*   **`live_trades.html`**:
    *   [x] Add sidebar HTML.
    *   [x] Reference `sidebar.css`.
    *   [x] Adjust layout for sidebar.
    *   [x] Remove old navigation links.

## 4. Verification Checkbox
*   [x] Sidebar appears on all 4 pages.
*   [x] Navigation links in sidebar work correctly.
*   [x] `activations_explorer.html` successfully loads and displays data.
*   [x] Layout remains responsive on different screen sizes.
