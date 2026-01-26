## Signal Generation Criteria (2025-11-07)

**Source:** User provided

**Logic:**
1.  Get the most recent 2 rows from the zone data.
2.  **Buy Signal:** `current s_g9 is null AND prev s_g9 > 0`
3.  **Sell Signal:** `current b_g9 is null AND prev b_g9 > 0`