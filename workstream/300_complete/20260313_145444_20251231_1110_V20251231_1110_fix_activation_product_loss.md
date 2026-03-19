# Plan: Fix Product-Scoped Activation Loss

This document outlines the plan to fix the bug where product-scoped activation lists were being stripped in the backend, leading to unintended "global" strategy activations.

## 1. Understanding of Requirements

*   The backend's `_coerce_activation_entry` function currently only extracts `active`, `activated_at`, and `manual` fields, effectively deleting the `products` list if it exists in `activations.json`.
*   This results in any active strategy being treated as active for ALL products.
*   The `_is_active` check also has a fallback that returns `True` if the `products` list is missing, which exacerbates the issue once the list is stripped.

## 2. Plan of Approach

1.  **Modify `_coerce_activation_entry` in `common.py`**:
    *   Update the function to preserve the `products` field.
2.  **Modify `_merge_activation_entries` in `common.py`**:
    *   Implement merging of `products` lists to avoid data loss during key normalization.
3.  **Tighten `_is_active` in `common.py`**:
    *   Change the fallback logic to return `False` if the `products` list is missing.
4.  **Update Version**:
    *   Update `VERSION` in `constants.py` to `V20251231_1110`.

## 3. List of Changes

### `common.py`

*   [ ] Update `_coerce_activation_entry` (around line 1224) to include `products`.
*   [ ] Update `_merge_activation_entries` (around line 1236) to merge `products` lists.
*   [ ] Update `_is_active` (around line 448) to return `False` as fallback.

### `constants.py`

*   [ ] Update `VERSION` to `V20251231_1110`.

## 4. Verification

*   Restart strategy scripts.
*   Verify that L-trades are only generated for products explicitly listed in `activations.json`.
