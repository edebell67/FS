# Add Momentum R Strategy Group Filter

Source: User request to modify `/realtime_stats.html` strategy group filtering to include `momentum_r`.

Task Type: standard

Task Attributes:
- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: false

Task Summary:
Add a new user-visible strategy group option for `momentum_r` in the Trade Performance Dashboard strategy group filter so reverse momentum strategy stats can be selected independently.

Context:
- `C:\Users\edebe\eds\TradeApps\breakout\fs\realtime_stats.html`
- API/dashboard data should expose or tolerate `momentum_r` as a selectable strategy group alongside existing groups: `all`, `momentum`, `breakout`, `breakout_r`, `breakout_rev`, and `breakout_r_rev`.

Destination Folder: `C:\Users\edebe\eds\TradeApps\breakout\fs`

Dependency: `C:\Users\edebe\eds\TradeApps\breakout\fs\momentum_r.py`

Plan:
- [x] 1. Inspect realtime stats strategy group option generation.
  - [x] Test: `Select-String -Path C:\Users\edebe\eds\TradeApps\breakout\fs\realtime_stats.html -Pattern "strategyGroupFilter|titleizeStrategyGroup|strategy_groups"` returns the relevant UI and JavaScript locations.
  - Evidence: Static select options, `titleizeStrategyGroup`, and `syncStrategyGroupFilter` identified in `realtime_stats.html`; API-owned group list identified in `trade_viewer_api.py`.
- [x] 2. Add `momentum_r` to the strategy group filter and display label mapping.
  - [x] Test: `Select-String -Path C:\Users\edebe\eds\TradeApps\breakout\fs\realtime_stats.html -Pattern "momentum_r"` shows the option and label mapping.
  - Evidence: `realtime_stats.html` contains `<option value="momentum_r">Momentum R</option>` and `momentum_r: 'Momentum R'`.
- [x] 3. Validate the page still parses and the filter remains compatible with API-driven group lists.
  - [x] Test: Review changed HTML/JS and, if API is running, request `/api/realtime_stats?strategy_group=momentum_r`; expected result is no frontend parsing issue and API accepts the group without breaking the dashboard response.
  - Evidence: `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py` passed; local API restarted and returned `success=True`, `selected_group=momentum_r`.

Evidence:
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: diff
  - Artifact: `git -C C:\Users\edebe\eds\TradeApps\breakout\fs diff -- realtime_stats.html trade_viewer_api.py`
  - Objective-Proved: Shows the UI and label changes required to expose `momentum_r`.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py` passed; direct import check returned `momentum_r` group, `momentum_r` match `True`, plain `momentum` match `False`.
  - Objective-Proved: Confirms the updated file contains `momentum_r` and validation was run.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: `http://localhost:5000/api/realtime_stats?strategy_group=momentum_r&product=` returned `success=True`, `selected_group=momentum_r`.
  - Objective-Proved: User can select `Momentum R` from the strategy group filter.
  - Status: captured

Implementation Log:
- 2026-04-29 14:54:22 - Task created from user request.
- 2026-04-29 16:55:31 - Implemented UI and API strategy group support for `momentum_r`; restarted local API to activate backend change.

Changes Made:
- `C:\Users\edebe\eds\TradeApps\breakout\fs\realtime_stats.html`
  - Added static `Momentum R` strategy group option.
  - Added `momentum_r` display label mapping.
- `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
  - Added `momentum_r` to `REALTIME_STATS_GROUP_OPTIONS`.
  - Added exact `momentum_r` classifier and excluded `momentum_r` from the plain `momentum` group.

Validation:
- `Select-String -Path C:\Users\edebe\eds\TradeApps\breakout\fs\realtime_stats.html -Pattern "momentum_r|Momentum R|strategyGroupFilter|titleizeStrategyGroup" -CaseSensitive:$false` confirmed UI option and label mapping.
- `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py` passed.
- `python -c "import trade_viewer_api as api; print([g for g in api.REALTIME_STATS_GROUP_OPTIONS if g['key']=='momentum_r']); print(api._realtime_name_matches_group('momentum_r_0_tp5.0_sl7.0','momentum_r')); print(api._realtime_name_matches_group('momentum_r_0_tp5.0_sl7.0','momentum'))"` returned `Momentum R`, `True`, `False`.
- `Invoke-RestMethod -Uri 'http://localhost:5000/api/realtime_stats?strategy_group=momentum_r&product='` returned `success=True`, `selected_group=momentum_r`.

Risks/Notes:
- Local API was restarted because the previously running server still returned the old group map.
- Existing uncommitted realtime stats snapshot-navigation/cache changes are present in the same files and were not reverted.

Completion Status:
Complete - 2026-04-29 16:55:31
