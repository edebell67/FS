Source: Direct user request in this session.

Task Summary: Add a Trade Bucket delta-basis option in the FS path so bucket action/leader selection can use either `delta 1` (`current net - start net`) or `delta 2` (`current net - creation net`). Default must be `delta 1`. The selected delta basis must remain the criterion used for trade selection/promotion.

Context:
- C:\Users\edebe\eds\TradeApps\breakout\fs\trade_bucket.html
- C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py
- C:\Users\edebe\eds\workstream\300_complete\20260313_135137_breakout_align_tb_and_multi_chart_bucket_behaviour.md

Plan:
- [ ] 1. Add persistent bucket-level delta-basis configuration with default `delta_1`.
  - Test: Create/load/update buckets and confirm the field is present and defaults correctly for legacy buckets.
  - Evidence: Pending.
- [ ] 2. Apply the selected delta basis to Trade Bucket leader selection and backend promotion/reconciliation logic.
  - Test: Confirm the same bucket chooses leaders from `current_net_from_chart` when `delta_1`, and from `net_delta_from_creation` when `delta_2`.
  - Evidence: Pending.
- [ ] 3. Add Trade Bucket UI controls so users can view/change the delta basis and understand which delta is currently driving trade selection.
  - Test: Confirm UI update persists via API and labels reflect the active basis.
  - Evidence: Pending.

Implementation Log:
- $(Get-Date -Format 'yyyy-MM-dd HH:mm zzz'): Created this task from the user request to make the Trade Bucket delta basis configurable while keeping the selected delta as the action criterion.

Changes Made:
- Created lifecycle task file only.

Validation:
- Task capture only; no code changes made.

Risks/Notes:
- Legacy buckets will need a backward-compatible default.
- Multi-chart remains delta-1-based by design; this task makes Trade Bucket selectable without changing multi-chart semantics.

Completion Status:
- In Progress - $(Get-Date -Format 'yyyy-MM-dd HH:mm zzz')
