Source: User request in Codex chat on 2026-05-11 to review the `ep_019` results.

Task Type: standard

Task Attributes:
- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: false

Task Summary: Review the current `ep_019` analysis results and producing scripts for correctness, statistical validity, and status consistency; report findings in code-review style.

Context:
- `epics/ep_019_breakout_monetization/preselection_loop_v5.py`
- `epics/ep_019_breakout_monetization/multi_move_analyzer_v6_12.py`
- Related `multi_move_analyzer_v6_*` variants
- `workstream/300_complete/20260508_193500_ep019_500_strategy_preselection_refined_target.md`
- `workstream/200_inprogress/20260508_203000_ep019_501_dynamic_path_analysis_multi_move_logic.md`

Destination Folder: None

Dependency: None

Plan:
- [x] 1. Inspect the latest result-generating scripts and their documented claims.
  - [x] Test: Read the current analyzers and identify the exact claims being made by the lifecycle files and script outputs.
  - [x] Evidence: Reviewed `preselection_loop_v5.py`, `multi_move_analyzer_v6_12.py`, `multi_move_analyzer_v6_11.py`, `multi_move_analyzer_v6_6.py`, and the lifecycle files for Tasks 500 and 501.
- [x] 2. Run targeted validation of the latest scripts and compare outputs to the documented claims.
  - [x] Test: Execute the current result scripts and capture the resulting metrics or failures.
  - [x] Evidence: Runtime outputs recorded below for `preselection_loop_v5.py`, `multi_move_analyzer_v6_12.py`, `multi_move_analyzer_v6_11.py`, and `multi_move_analyzer_v6_6.py`.
- [x] 3. Produce a review with findings ordered by severity and note residual risks.
  - [x] Test: Cross-check code behavior against claimed methodology, sample sizes, and success criteria.
  - [x] Evidence: Findings recorded below and summarized in final response.

Evidence:
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: file_output
  - Artifact: `epics/ep_019_breakout_monetization/preselection_loop_v5.py`, `multi_move_analyzer_v6_6.py`, `multi_move_analyzer_v6_11.py`, `multi_move_analyzer_v6_12.py`, and the Task 500/501 lifecycle files
  - Objective-Proved: Relevant scripts and lifecycle records were reviewed.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: Runtime outputs from `python preselection_loop_v5.py`, `python multi_move_analyzer_v6_12.py`, `python multi_move_analyzer_v6_11.py`, and `python multi_move_analyzer_v6_6.py`
  - Objective-Proved: Runtime validation confirms or contradicts the documented results.
  - Status: captured

Implementation Log:
- 2026-05-11 19:35:09: Review task created for `ep_019` result review.
- 2026-05-11 19:38: Executed `preselection_loop_v5.py`; current output analyzed 10 unique days and reported `balanced_50` at 5 AM as 83.3% (5/6), not 85.7% (6/7).
- 2026-05-11 19:38: Executed `multi_move_analyzer_v6_12.py`; current output showed 12.5% accuracy (1/8) with total real profit of `-$2447.50`.
- 2026-05-11 19:40: Executed adjacent revisions `v6.6` and `v6.11` to compare result volatility and confirm methodology drift.
- 2026-05-11 19:42: Confirmed configured non-DB search roots currently have zero qualifying `_summary_net.json` day folders, so the scripts are effectively evaluating DB data only.
- 2026-05-11 19:43: Confirmed `2026-01-24` and `2026-01-31` contain empty `strategies` payloads; multi-move analyzers silently drop them from the denominator by filtering out `None` results.

Changes Made:
- None yet.

Validation:
- `python C:\Users\edebe\eds\epics\ep_019_breakout_monetization\preselection_loop_v5.py`
  - Result: Loaded 10 unique days. Best result with minimum 5 samples was `balanced_50 h=5` at `83.3% (5/6)`.
- `python C:\Users\edebe\eds\epics\ep_019_breakout_monetization\multi_move_analyzer_v6_12.py`
  - Result: `FINAL GLOBAL ACCURACY: 12.5% (1/8)`, `TOTAL REAL PROFIT: $-2447.50`.
- `python C:\Users\edebe\eds\epics\ep_019_breakout_monetization\multi_move_analyzer_v6_11.py`
  - Result: `FINAL GLOBAL ACCURACY: 37.5% (3/8)`, `TOTAL PROFIT (Realised): $2147.50`.
- `python C:\Users\edebe\eds\epics\ep_019_breakout_monetization\multi_move_analyzer_v6_6.py`
  - Result: `FINAL GLOBAL ACCURACY: 28.6% (2/7)`, `TOTAL PROFIT/LOSS: $72.50`.
- Data-root inspection
  - Result: `fs/json/live/forex` and `fs/json/live/social_posting_package` currently have zero qualifying day folders with `_summary_net.json`; `DB/json/live` currently has 10.
- Empty-day inspection
  - Result: `2026-01-24` and `2026-01-31` `_summary_net.json` files contain `strategies=0`, so those days are omitted from analyzer result sets.

Risks/Notes:
- The review may uncover result inflation or methodological inconsistencies rather than implementation bugs alone.
- Current lifecycle claims for Task 500 and Task 501 are not aligned with current script outputs.
- Result quality is highly sensitive to data availability in configured roots and to whether empty days are counted or silently dropped.

Findings Summary:
- High: Task 500’s documented result is stale versus current runtime output.
- High: `multi_move_analyzer_v6_11.py` overstates profit by summing only positive raw nets while labeling the total as realised profit.
- Medium: `multi_move_analyzer_v6_12.py` and related analyzers silently remove empty days from the denominator, inflating reported hit rates.
- Medium: Task 501’s lifecycle record does not reflect the later analyzer revisions now present in the epic folder.

Completion Status:
- Complete on 2026-05-11 19:44 after runtime validation and review synthesis.
