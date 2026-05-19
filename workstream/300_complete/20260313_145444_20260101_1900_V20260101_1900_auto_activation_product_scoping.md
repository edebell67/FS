# Plan: Implement Top-Product Scoping for Auto-Activation

This document outlines the plan to modify the auto-activation logic so that it specifically activates the **top-performing product** for each strategy, and ensures that if ranking changes, the product is updated.

## 1. Understanding of Requirements

*   **Goal**: When a strategy (`key`) is auto-activated, it should only be active for the product that is currently performing best for that specific strategy.
*   **Behavior**: If Strategy A's best product is "AUD" in Minute 1, it should activate "AUD". If "NZD" takes the lead in Minute 2, "NZD" should replace "AUD" in the `activations.json` record.
*   **Current State**: The backend currently activates the strategy key generally, but the trade engine requires a `products` list for strict scoping.

## 2. Plan of Approach

1.  **Modify `_activation_record`**:
    *   Update the function to accept an optional `products` list.
2.  **Modify `_perform_auto_activation_check`**:
    *   In the candidacy loop (Net and Alt), identify the single product with the highest P&L for each candidate `key`.
    *   Store this "top product" alongside the candidate key.
    *   When creating the `updates` record, pass the `top_product` (as a single-item list) to `_activation_record`.
3.  **Update Version**:
    *   Increment the version in `constants.py` to `V20260101_1900`.

## 3. List of Changes

### `common.py`

*   [ ] Update `_activation_record` to handle `products`.
*   [ ] Update `net_candidates_raw` and `alt_candidates_raw` to store the top-performing product.
*   [ ] Update the `newly_activated` sets to store tuples or dicts containing the key and product.
*   [ ] Update the final record creation in `updates` to include the `products` list.

### `constants.py`

*   [ ] Update `VERSION` to `V20260101_1900`.

## 4. Verification

*   Check `activations.json` after a backend cycle.
*   Verify that `manual: false` records now contain a `products` array with the best-performing product.
*   Verify that if another product takes the lead, the list in `activations.json` is updated.
