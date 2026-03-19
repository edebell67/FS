# Plan: Refine Trade Bucket Activation - Top Performer Only

This plan outlines the changes to the Trade Bucket activation logic to ensure only the single best-performing strategy in a bucket is promoted to live trading, and only if it exceeds the user-defined threshold.

## 1. Understanding of Requirements
Currently, the trade bucket system activates *all* strategies in a bucket that meet the minimum net return threshold. 
The requirement is to refine this to:
- Evaluate all strategies in the bucket.
- Identify the strategy with the **maximum** performance gain (`perf_diff`) since the bucket start time.
- Promote **only this single top performer** to `activations_is_live.json`, provided its gain is greater than or equal to the `minimum_difference` (L-trade threshold).

## 2. List of Changes

### `trade_viewer_api.py`
- [ ] Modify `_sync_bucket_to_activations`:
    - Changed from an "all that match" loop to a "find the max" process.
    - Store the `candidate` strategy information and its `perf_diff`.
    - Compare `max_perf_diff` against `min_diff` after the loop.
    - Write only the top-performing record if it meets the criteria.

### `Constants.py`
- [ ] Update version to `V20260123_0010`.

## 3. Verification
- Create a bucket with multiple strategies.
- Verify through logs (or `activations_is_live.json`) that only the strategy with the highest net gain is picked.
- Verify that if no strategy exceeds the threshold, no records are written.
- Verify that toggling the bucket OFF still clears all associated records.
