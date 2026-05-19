# Strategy Pre-Selection Monetization Discovery

## Source
- Analysis session 2026-05-06/07
- Reference: `20260506_184700_breakout_997_strategy_gap_analysis_methodology.md`

## Task Type
looping

## Task Attributes
- `looping_task: true`
- `loop_until: condition_met`
- `loop_interval: immediate`
- `max_iterations: 20`

## Task Summary
Discover a reliable method to pre-select forex strategies that end the trading day with net > $350 at 90% accuracy. This is a looping task that iterates through different parameter combinations and analytical approaches until a sustained solution is found or max iterations reached.

## Context
- **Data Source**: `TradeApps/breakout/fs/json/live/forex/{date}/_summary_net.json`
- **Available Dates**: Multiple trading days in `2026-05-*` folders
- **Goal**: Monetize early-session signals to predict EOD winners

## Destination Folder
epics/ep_019_breakout_monetization/

## Dependency
- `20260506_184700_breakout_997_strategy_gap_analysis_methodology.md` (analysis methodology)

---

## Success Criteria

| Criterion | Target | Measurement |
|-----------|--------|-------------|
| EOD net threshold | > $350 | Selected strategies end day above threshold |
| Accuracy | >= 90% | % of selected strategies hitting threshold |
| Consistency | Multi-day | Works across 5+ trading days |
| Improvement | Each iteration | Results must improve or discard approach |

## Alternative Success Criteria (if primary not achievable)

| Criterion | Target | Example Output |
|-----------|--------|----------------|
| Top quartile selection | 25% of winners | "Selected 25% winning strategies with +$350" |
| Improvement prediction | +$100 gain | "Selected strategies +100 improvement 80%" |

---

## Loop Execution Framework

### Iteration Structure
```
LOOP (max 20 iterations):
  1. Load parameters from previous iteration (or defaults)
  2. Run analysis script
  3. Evaluate results against success criteria
  4. IF improved OR meets criteria:
       - Record as best result
       - IF meets final criteria: EXIT with SUCCESS
  5. ELSE:
       - Discard approach
       - Modify parameters
  6. Log iteration result
  7. Continue to next iteration
```

### Parameter Space to Explore

| Parameter | Initial | Range | Purpose |
|-----------|---------|-------|---------|
| `cutoff_hour` | 3 | 1-8 | Hour to evaluate early signals |
| `min_gap_threshold` | 30 | 10-500 | Minimum gap over #2 to consider leader |
| `min_net_at_cutoff` | 100 | 50-500 | Minimum net value at cutoff |
| `metric` | net | net, buy_net, sell_net | Which metric to rank by |
| `lookback_consistency` | 2 | 1-5 | Hours leader must hold position |
| `pair_filter` | all | specific pairs | Focus on specific currency pairs |
| `strategy_type_filter` | all | R, Rev, momentum | Strategy family filter |
| `top_n_select` | 5 | 1-10 | How many top strategies to select |
| `gap_over_3rd` | 0 | 0-200 | Require gap over 3rd place |

---

## Analysis Script Template

**Location**: `epics/ep_breakout_monetization/preselection_analyzer.py`

```python
#!/usr/bin/env python3
"""
Strategy Pre-Selection Analyzer
Looping task iteration script - token efficient
"""
import json
import os
from datetime import datetime
from pathlib import Path

# === PARAMETERS (modify per iteration) ===
PARAMS = {
    "cutoff_hour": 5,
    "min_gap_threshold": 30,
    "min_net_at_cutoff": 100,
    "metric": "net",
    "lookback_consistency": 2,
    "top_n_select": 5,
    "eod_target": 350,
    "accuracy_target": 0.90
}

DATA_DIR = Path("TradeApps/breakout/fs/json/live/forex")
DATES = []  # Populated dynamically

def load_day(date_str):
    """Load summary_net.json for a date."""
    path = DATA_DIR / date_str / "_summary_net.json"
    if not path.exists():
        return None
    with open(path) as f:
        return json.load(f)

def get_best_at_cutoff(data, cutoff_dt, metric="net"):
    """Get best record per strategy/pair up to cutoff."""
    best = {}
    for strat, pairs in data.get("strategies", {}).items():
        for pair, recs in pairs.items():
            for r in recs:
                t = datetime.fromisoformat(r["t"])
                if t <= cutoff_dt:
                    key = (strat, pair)
                    if key not in best or r[metric] > best[key][metric]:
                        best[key] = {**r, "strategy": strat, "pair": pair}
    return best

def get_eod(data):
    """Get EOD record per strategy/pair."""
    eod = {}
    for strat, pairs in data.get("strategies", {}).items():
        for pair, recs in pairs.items():
            if recs:
                eod[(strat, pair)] = {**recs[-1], "strategy": strat, "pair": pair}
    return eod

def select_strategies(best_at_cutoff, params):
    """Apply selection criteria to pick candidate strategies."""
    candidates = []
    sorted_by_metric = sorted(best_at_cutoff.values(),
                               key=lambda x: x[params["metric"]],
                               reverse=True)

    if len(sorted_by_metric) < 2:
        return []

    # Calculate gap
    top = sorted_by_metric[0]
    second = sorted_by_metric[1]
    gap = top[params["metric"]] - second[params["metric"]]

    # Apply filters
    for i, s in enumerate(sorted_by_metric[:params["top_n_select"]]):
        if s[params["metric"]] >= params["min_net_at_cutoff"]:
            if i == 0 and gap >= params["min_gap_threshold"]:
                candidates.append({"rank": i+1, "gap": gap, **s})
            elif i > 0:
                candidates.append({"rank": i+1, "gap": 0, **s})

    return candidates

def evaluate_selections(selections, eod_data, params):
    """Check how selections performed at EOD."""
    results = []
    for sel in selections:
        key = (sel["strategy"], sel["pair"])
        if key in eod_data:
            eod_net = eod_data[key]["net"]
            hit_target = eod_net >= params["eod_target"]
            results.append({
                "strategy": sel["strategy"],
                "pair": sel["pair"],
                "cutoff_net": sel["net"],
                "eod_net": eod_net,
                "change": eod_net - sel["net"],
                "hit_target": hit_target
            })
    return results

def run_iteration(params, dates):
    """Run one iteration across all dates."""
    all_results = []

    for date_str in dates:
        data = load_day(date_str)
        if not data:
            continue

        # Build cutoff datetime
        cutoff_dt = datetime.fromisoformat(f"{date_str}T{params['cutoff_hour']:02d}:00:00")

        best = get_best_at_cutoff(data, cutoff_dt, params["metric"])
        eod = get_eod(data)
        selections = select_strategies(best, params)
        results = evaluate_selections(selections, eod, params)

        all_results.append({
            "date": date_str,
            "selections": len(selections),
            "results": results,
            "hits": sum(1 for r in results if r["hit_target"]),
            "total": len(results)
        })

    return all_results

def calculate_metrics(all_results, params):
    """Calculate overall accuracy and summary."""
    total_hits = sum(r["hits"] for r in all_results)
    total_selections = sum(r["total"] for r in all_results)

    if total_selections == 0:
        return {"accuracy": 0, "total": 0, "hits": 0, "meets_criteria": False}

    accuracy = total_hits / total_selections
    meets = accuracy >= params["accuracy_target"]

    return {
        "accuracy": accuracy,
        "total": total_selections,
        "hits": total_hits,
        "meets_criteria": meets,
        "params": params
    }

def main():
    # Find available dates
    dates = sorted([d.name for d in DATA_DIR.iterdir() if d.is_dir() and d.name.startswith("2026")])

    results = run_iteration(PARAMS, dates)
    metrics = calculate_metrics(results, PARAMS)

    # Output results
    print(f"=== ITERATION RESULT ===")
    print(f"Params: cutoff={PARAMS['cutoff_hour']}h, gap>={PARAMS['min_gap_threshold']}, net>={PARAMS['min_net_at_cutoff']}")
    print(f"Accuracy: {metrics['accuracy']*100:.1f}% ({metrics['hits']}/{metrics['total']})")
    print(f"Target: {PARAMS['accuracy_target']*100:.0f}% with EOD > ${PARAMS['eod_target']}")
    print(f"MEETS CRITERIA: {metrics['meets_criteria']}")

    # Detail per day
    for r in results:
        hits = r["hits"]
        total = r["total"]
        pct = (hits/total*100) if total > 0 else 0
        print(f"  {r['date']}: {hits}/{total} ({pct:.0f}%)")

    return metrics

if __name__ == "__main__":
    main()
```

---

## Iteration Log

| Iter | Parameters | Accuracy | Hits/Total | Improved | Action |
|------|------------|----------|------------|----------|--------|
| 1 | h=3,gap>=30,net>=100,net,top1 | 25.0% | 1/4 | YES | baseline |
| 2 | h=4,gap>=30,net>=100,net,top1 | 50.0% | 1/2 | YES | |
| 3 | h=5,gap>=30,net>=100,net,top1 | 25.0% | 1/4 | | |
| 4 | h=6,gap>=30,net>=100,net,top1 | 50.0% | 1/2 | | |
| 5 | h=5,gap>=0,net>=100,net,top1 | 37.5% | 3/8 | | |
| 6 | h=5,gap>=50,net>=100,net,top1 | 33.3% | 1/3 | | |
| 7 | h=5,gap>=100,net>=100,net,top1 | 50.0% | 1/2 | | |
| 8 | h=5,gap>=200,net>=100,net,top1 | 50.0% | 1/2 | | |
| 9 | h=5,gap>=50,net>=50,net,top1 | 33.3% | 1/3 | | |
| 10 | h=5,gap>=50,net>=100,net,top1 | 33.3% | 1/3 | | |
| 11 | h=5,gap>=50,net>=200,net,top1 | 33.3% | 1/3 | | |
| 12 | h=5,gap>=50,net>=300,net,top1 | 33.3% | 1/3 | | |
| 13 | h=5,gap>=50,net>=100,net,top1 | 33.3% | 1/3 | | |
| 14 | h=5,gap>=50,net>=100,buy_net,top1 | 50.0% | 1/2 | | |
| 15 | h=5,gap>=50,net>=100,sell_net,top1 | 16.7% | 1/6 | | |
| 16 | h=5,gap>=30,net>=100,net,top1 | 25.0% | 1/4 | | |
| 17 | h=5,gap>=30,net>=100,net,top3 | 25.0% | 3/12 | | |
| 18 | h=5,gap>=30,net>=100,net,top5 | 20.0% | 4/20 | | |
| 19 | h=4,gap>=100,net>=50,net,top1 | 100.0% | 1/1 | YES | LOW SAMPLE |
| 20 | h=3,gap>=200,net>=100,net,top1 | 0.0% | 0/0 | | no data |

---

## Best Result Tracker

```
best_accuracy: 100.0%
best_params: {cutoff_hour: 4, min_gap: 100, min_net: 50, metric: net, top_n: 1}
best_iteration: 19
solution_found: true (BUT LOW SAMPLE SIZE - 1/1)
```

## Statistical Concern
- Iteration 19 achieved 100% but with only 1 selection across 10 days
- Only 2026-05-04 qualified under strict parameters
- More robust candidates at 50% accuracy with 1/2 or 2/4 samples:
  - Iter 2: h=4,gap>=30,net>=100 (50%, 1/2)
  - Iter 7: h=5,gap>=100,net>=100 (50%, 1/2)
  - Iter 8: h=5,gap>=200,net>=100 (50%, 1/2)

---

## Output Format Per Iteration

```
ITERATION {n} RESULT:
- Parameters: {param_summary}
- Accuracy: {accuracy}% ({hits}/{total})
- vs Previous: {+/-change}%
- Status: IMPROVED / DISCARDED / SOLUTION_FOUND
- Output: "Successfully selected {x}% winning strategies with +${amount}"
```

---

## Exit Conditions

1. **SUCCESS**: Accuracy >= 90% with EOD > $350 across 5+ days
2. **PARTIAL SUCCESS**: Accuracy >= 80% with any improvement metric
3. **MAX ITERATIONS**: 20 iterations reached without solution
4. **NO IMPROVEMENT**: 5 consecutive iterations without improvement

---

## On Solution Found

Generate skill file at: `skills/strategy-preselection/SKILL.md`

```markdown
---
name: strategy-preselection
description: Pre-select forex strategies likely to end day with net > $350
---

# Strategy Pre-Selection Skill

## Trigger
Use when selecting strategies at market open for day trading.

## Process
1. Load _summary_net.json at cutoff hour
2. Apply selection criteria: {winning_params}
3. Output selected strategy/pair combinations

## Parameters
{final_params}

## Expected Accuracy
{final_accuracy}%
```

---

## On No Solution Found

Update this task with:
1. Best parameters found
2. Accuracy achieved
3. Recommended parameter variations for next run
4. Insights on what signals correlate with success

---

## Plan

- [x] 1. Create analysis script at destination folder
  - Test: Script runs without error
  - Evidence: `epics/ep_019_breakout_monetization/preselection_loop.py` created and executed
- [x] 2. Run iteration 1 (baseline parameters)
  - Test: Produces accuracy metric
  - Evidence: Iteration 1: 25.0% (1/4)
- [x] 3. Loop iterations 2-20, adjusting parameters
  - Test: Each iteration logged
  - Evidence: All 20 iterations logged in Iteration Log table
- [x] 4. Evaluate final result
  - Test: Solution found OR best result documented
  - Evidence: Best Result Tracker updated - 100% (1/1) but low sample
- [ ] 5. Generate skill OR document next steps
  - Test: Output artifact created
  - Evidence: Next run parameters documented (no skill - insufficient confidence)

## Evidence
- Evidence-Type: file_output
  - Artifact: `epics/ep_019_breakout_monetization/preselection_loop.py`
  - Objective-Proved: Loop execution framework implemented
  - Status: captured
- Evidence-Type: log_output
  - Artifact: 20 iterations completed, best 100% (1/1), practical best 50% (1/2)
  - Objective-Proved: Parameter space explored systematically
  - Status: captured

Objective-Delivery-Coverage: 40%
Auto-Acceptance: false

## Implementation Log
- 2026-05-07 09:42: Task created with looping framework
- 2026-05-07 09:48: Loop executed 20 iterations
- 2026-05-07 09:50: Results logged, best accuracy 100% but low sample (1/1)

## Changes Made
- Created: `workstream/100_backlog/20260507_094248_breakout_500_strategy_preselection_monetization.md`
- Created: `epics/ep_019_breakout_monetization/preselection_loop.py`
- Updated: `skills/workstream-task-lifecycle/SKILL.md` (added _500_ looping task reference)

## Validation
- 20 iterations completed successfully
- Best parameters: h=4, gap>=100, net>=50 (100% but 1/1 sample)
- Practical best: h=4-6, gap>=100-200 (50% with 1/2 samples)

## Next Run Parameters (for continuation)
Since 90% accuracy not achieved with sufficient samples, next _500_ run should:
1. Lower EOD target from $350 to $200 or $100
2. Track improvement over cutoff instead of absolute EOD
3. Add more dates (need 20+ days for statistical significance)
4. Try composite signals (gap + consistency duration)
5. Focus on Monday-like days (clear early separation)

## Risks/Notes
- Token efficiency critical - use code-based analysis, minimize verbose output
- Large JSON files require efficient loading
- May need to expand date range if insufficient data
- 90% accuracy target is aggressive - may need to relax
- **Key insight**: Higher gap thresholds achieve 50% but reduce frequency
- **Key insight**: Only Monday 2026-05-04 had clear early separation

## Completion Status
Partial Complete - 2026-05-07
- Loop executed 20 iterations
- No robust solution found (100% with 1 sample not statistically valid)
- 50% accuracy achievable with gap>=100 parameters
- Recommend: Continue with lower EOD target OR more trading days
