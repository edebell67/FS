# Plan: Enhance `tradeable_product_list` Logic in `sp_001_zone_distribution_trade` (Revised for Backward Compatibility)

**Date:** 2025-11-07 15:30 (Revised)

**Version:** X

## 1. Understanding of Requirements

The goal is to enhance the flexibility of the `tradeable_product_list` configuration in `dbo.config` for the `sp_001_zone_distribution_trade` stored procedure. The new logic should support:

*   **Wildcard Inclusion (`**`):** If the `tradeable_product_list` contains `'**'`, all products that meet other trading criteria should be considered tradeable by default.
*   **Explicit Exclusion (`-{product}`):** If the `tradeable_product_list` contains `'-{product}'` (e.g., `'-eur'`), that specific product must be excluded from trading. This exclusion rule takes precedence over the `'**'` wildcard.
*   **Existing Explicit Inclusion:** The current functionality of explicitly listing product names (e.g., `'eur', 'gbp'`) for inclusion should remain valid and function as before when the `'**'` wildcard is not present.

**Crucial Additional Requirement:** Ensure backward compatibility. Other stored procedures that interact with the whitelist using the current approach and the `in_whitelist` helper (`@wl_all`) must continue to work as is.

## 2. Plan of Approach

The core of this enhancement will involve modifying how the `tradeable_product_list` is parsed and how the `in_whitelist` flag is determined *specifically within `sp_001_zone_distribution_trade`*.

1.  **Retain Existing Whitelist Parsing:** The existing `@trade_product_list_raw` and `@tpl_clean` variables, along with the `@wl_all` helper, will be kept as is to ensure backward compatibility for other stored procedures.
2.  **Introduce New Parsing for `sp_001_zone_distribution_trade`:**
    *   *Within `sp_001_zone_distribution_trade`*, after the initial `@tpl_clean` is derived, we will parse `@tpl_clean` further to identify:
        *   The presence of the `'**'` wildcard.
        *   Explicit exclusion entries (starting with `'-'`).
        *   Explicit inclusion entries (regular product names).
    *   These will be stored in appropriate temporary tables or flags (`@include_all_products`, `#ExcludedProducts`, `#IncludedProducts`).
3.  **Modify `in_whitelist` logic *only within `sp_001_zone_distribution_trade`*:**
    *   The `in_whitelist` column in the `#cand` temporary table (and subsequently in `#filtered_candidates`) will be calculated based on a combined logic:
        *   If `@wl_all` is `1` (meaning the original `tradeable_product_list` was empty), then the new wildcard/exclusion logic applies: A product is `in_whitelist = 1` unless it is found in the explicit exclusion list.
        *   If `@wl_all` is `0` (meaning the original `tradeable_product_list` had explicit entries), then the new wildcard/exclusion logic applies:
            *   If `'**'` is present: A product is `in_whitelist = 1` unless it is found in the explicit exclusion list.
            *   If `'**'` is *not* present: A product is `in_whitelist = 1` only if it is found in the explicit inclusion list.
        *   Explicit exclusions always override inclusions.

## 3. List of Changes

*   **`db_scripts/dbo.sp_001_zone_distribution_trade.StoredProcedure.sql`**:
    *   [x] **Retain existing `@wl_all` declaration and calculation.**
    *   [x] **Declare new variables:**
        *   `@include_all_products BIT` to store whether `'**'` is present in `@tpl_clean`.
        *   Temporary table `#ExcludedProducts (product_name nvarchar(50) PRIMARY KEY)` to store products to be excluded from `@tpl_clean`.
        *   Temporary table `#IncludedProducts (product_name nvarchar(50) PRIMARY KEY)` to store products explicitly included from `@tpl_clean` (when `'**'` is not present).
    *   [x] **Modify `trade_product_list` parsing (new logic):**
        *   After `@tpl_clean` is derived, iterate through its comma-separated values.
        *   If a value is `'**'`, set `@include_all_products = 1`.
        *   If a value starts with `'-'`, insert the rest of the string into `#ExcludedProducts`.
        *   Otherwise, insert the value into `#IncludedProducts`.
    *   [x] **Update `in_whitelist` calculation in `INSERT #cand`:**
        *   Modify the `CASE` statement for `in_whitelist` to implement the combined logic:
            ```sql
            CASE
                WHEN @wl_all = 1 THEN -- Original list was empty, so new logic applies
                    CASE
                        WHEN EXISTS (SELECT 1 FROM #ExcludedProducts WHERE product_name = LOWER(pf.product)) THEN 0 -- Explicitly excluded
                        ELSE 1 -- Included by default
                    END
                ELSE -- Original list had explicit entries, so new logic applies to those entries
                    CASE
                        WHEN EXISTS (SELECT 1 FROM #ExcludedProducts WHERE product_name = LOWER(pf.product)) THEN 0 -- Explicitly excluded
                        WHEN @include_all_products = 1 THEN 1 -- Included by wildcard
                        WHEN EXISTS (SELECT 1 FROM #IncludedProducts WHERE product_name = LOWER(pf.product)) THEN 1 -- Explicitly included
                        ELSE 0 -- Not included
                    END
            END
            ```