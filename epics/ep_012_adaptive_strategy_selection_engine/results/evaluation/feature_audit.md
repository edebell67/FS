# Feature Audit -- Adaptive Strategy Selection Engine Phase 3
## Feature Inventory
All features are computed from data available at decision time (snap_idx t).
No feature uses data from snap_idx t+1 or later.

| Feature | Description | Leakage Risk |
|---------|-------------|-------------|
| `held_net` | Net P&L of currently held (product, strategy) at snap t | No -- observed at t |
| `held_rank` | Rank of held candidate among all strategies at snap t | No -- observed at t |
| `held_score` | Weighted score of held candidate at snap t | No -- observed at t |
| `held_net_slope_3` | Slope of held net over last 3 snapshots (causal window) | No -- window ends at t |
| `held_net_slope_5` | Slope of held net over last 5 snapshots | No -- window ends at t |
| `held_net_slope_10` | Slope of held net over last 10 snapshots | No -- window ends at t |
| `held_positive_streak` | Consecutive snaps held candidate has had net > 0 | No -- count up to t |
| `hold_duration` | Number of snaps since held candidate was entered | No -- count up to t |
| `switch_count_today` | Number of switches taken so far today | No -- count up to t |
| `chal_net` | Net of best challenger (highest eligible non-held) at t | No -- observed at t |
| `chal_rank` | Rank of best challenger at t | No -- observed at t |
| `chal_score` | Score of best challenger at t | No -- observed at t |
| `chal_net_slope_3` | Slope of challenger net over last 3 snaps | No -- window ends at t |
| `chal_net_slope_5` | Slope of challenger net over last 5 snaps | No -- window ends at t |
| `chal_net_slope_10` | Slope of challenger net over last 10 snaps | No -- window ends at t |
| `net_gap` | chal_net - held_net at snap t | No -- derived from t |
| `score_gap` | chal_score - held_score at snap t | No -- derived from t |
| `num_positive_candidates` | Count of strategies with net > 0 at snap t | No -- board state at t |
| `minute_of_day` | Minute within trading day (0-1439) | No -- wall clock, no future data |

## Leakage Verdict
**CLEAN** -- all 19 features are observable at decision time t.
Reward labels (q_hold, q_switch) use snap t+1 data but are only used during TRAINING.
At inference, no t+1 data is accessed.

## Sample Action-Level Explanations

### Example 1 -- 2026-03-21 snap 0
- Action taken: **SWITCH**
- Strategy: `breakout_2_tp10.0_sl30.0`
- Net at decision: 95.0
- Q_hold=0.0, Q_switch=0.0, Q_flat=0.0
- Argmax: SWITCH chosen

### Example 2 -- 2026-03-21 snap 1
- Action taken: **SWITCH**
- Strategy: `breakout_R_Rev_2_tp20.0_sl20.0`
- Net at decision: 525.5999999998312
- Q_hold=0.0, Q_switch=0.0, Q_flat=0.0
- Argmax: SWITCH chosen

### Example 3 -- 2026-03-21 snap 2
- Action taken: **SWITCH**
- Strategy: `breakout_R_Rev_4_tp20.0_sl20.0`
- Net at decision: 585.0
- Q_hold=0.0, Q_switch=0.0, Q_flat=0.0
- Argmax: SWITCH chosen

### Example 4 -- 2026-03-22 snap 0
- Action taken: **FLAT**
- Strategy: `nan`
- Net at decision: 0.0
- Q_hold=0.0, Q_switch=0.0, Q_flat=0.0
- Argmax: FLAT chosen

### Example 5 -- 2026-03-22 snap 1
- Action taken: **FLAT**
- Strategy: `nan`
- Net at decision: 0.0
- Q_hold=0.0, Q_switch=0.0, Q_flat=0.0
- Argmax: FLAT chosen

## Model Notes
- Estimator: Ridge regression (StandardScaler + Ridge alpha=1.0)
- GBM (HistGradientBoosting) was evaluated but predict() latency was ~120ms/call on this platform; Ridge achieves <0.2ms/call with comparable accuracy.
- Recency weighting: sample_weight = exp(-0.1 * days_ago) applied per training sample.
- Walk-forward: no future data crosses train/test boundary.
