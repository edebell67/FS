# Epic 016 Marketing Stats Pack - Metric Catalog
# Date: 2026-05-04
# Version: V20260504_1300

## 1. Core Run Stats
| Metric ID | Display Name | Category | Business Purpose | User Facing Definition | Technical Definition | Calculation Type | Formula | Primary Source | Mode Safety |
|-----------|--------------|----------|------------------|-----------------------|----------------------|------------------|---------|----------------|-------------|
| `run_mode` | Engine Mode | Core | Show if engine is live or simulating | Whether the engine is watching live markets or historical data | Current mode from newest snapshot | boolean/label | `LATEST market_mode` | `frequency_snapshots` | `safe` |
| `engine_status` | Status | Core | Show operational health | Current status of the pattern engine (Active/Stopped/Degraded) | Health derived from snapshot freshness | label | `CASE WHEN last_write < 6m THEN 'Active' ELSE 'Stale' END` | `frequency_snapshots` | `safe` |
| `last_snapshot_time` | Last Snapshot | Core | Show data recency | Time of the most recent market snapshot processed | Max snapshot_time | timestamp | `MAX(snapshot_time)` | `frequency_snapshots` | `safe` |
| `products_active` | Active Products | Core | Show coverage breadth | Number of financial products currently being monitored | Count of products with fresh snapshots | count | `COUNT(DISTINCT product_id) WHERE snapshot_time > NOW() - 15m` | `frequency_snapshots` | `safe` |
| `total_snapshots` | Snapshot Volume | Core | Show database depth | Total number of market structural snapshots captured | Row count | count | `COUNT(*)` | `frequency_snapshots` | `safe` |
| `data_freshness` | Freshness (sec) | Core | Precise latency check | Seconds since the last market structure update | Current time minus max snapshot time | duration | `NOW() - MAX(snapshot_time)` | `frequency_snapshots` | `safe` |

## 2. Coverage Stats
| Metric ID | Display Name | Category | Business Purpose | User Facing Definition | Technical Definition | Mode Safety |
|-----------|--------------|----------|------------------|-----------------------|----------------------|-------------|
| `products_monitored` | Monitored Markets | Coverage | Scale of monitoring | Total number of configured products | `COUNT(*) FROM products WHERE is_active=TRUE` | `safe` |
| `products_with_turns` | Turn-Active Markets | Coverage | Show turn detection diversity | Products that have produced at least one turning point | `COUNT(DISTINCT product_id) FROM turning_points` | `safe` |
| `turn_coverage_pct` | Coverage Rate | Coverage | Percentage of markets with patterns | Ratio of turn-active markets to total monitored | `(products_with_turns / products_monitored) * 100` | `safe` |
| `products_with_vectors` | Profiled Markets | Coverage | Show pattern matching scale | Products with processed structural vectors | `COUNT(DISTINCT product_id) FROM pattern_vectors` | `safe` |

## 3. Turn Detection Stats
| Metric ID | Display Name | Category | Business Purpose | User Facing Definition | Technical Definition | Mode Safety |
|-----------|--------------|----------|------------------|-----------------------|----------------------|-------------|
| `total_turns_detected` | Patterns Detected | Detection | Headline "volume" number | Total market turning points identified by the engine | `COUNT(*) FROM turning_points` | `safe` |
| `total_tops` | Tops Identified | Detection | Directional balance | Total bearish/reversal peaks detected | `COUNT(*) WHERE turn_type='TOP'` | `safe` |
| `total_bottoms` | Bottoms Identified | Detection | Directional balance | Total bullish/reversal troughs detected | `COUNT(*) WHERE turn_type='BOTTOM'` | `safe` |
| `turns_last_24h` | Turns (24h) | Detection | Show daily activity | Incremental patterns found in the last day | `COUNT(*) WHERE turn_time > NOW() - 24h` | `safe` |
| `avg_turns_per_hour` | Turn Creation Rate | Detection | Show engine frequency | Mean turn creation per hour of operation | `total_turns / (run_duration_hours)` | `safe` |

## 4. Turn Quality Stats
| Metric ID | Display Name | Category | Business Purpose | User Facing Definition | Technical Definition | Mode Safety |
|-----------|--------------|----------|------------------|-----------------------|----------------------|-------------|
| `avg_confirm_delay` | Confirm Delay (min) | Quality | Show engine speed | Average time taken to confirm a pattern is real | `AVG(confirmation_delay_minutes)` | `safe` |
| `fast_confirm_rate` | Speed of Confidence | Quality | Show rapid reaction | % of turns confirmed in 1-2 snapshots | `(COUNT(delay < 10m) / total_turns) * 100` | `safe` |
| `avg_pattern_quality` | Pattern Integrity | Quality | Structural validity | Mean structural quality score (0.0 to 1.0) | `AVG(pattern_quality_score)` | `safe` |

## 5. Live Pattern Stats
| Metric ID | Display Name | Category | Business Purpose | User Facing Definition | Technical Definition | Mode Safety |
|-----------|--------------|----------|------------------|-----------------------|----------------------|-------------|
| `live_candidates` | Live Patterns | Live | Show current alerts | Number of products showing potential patterns NOW | `COUNT(*) FROM live_pattern_windows WHERE latest_snapshot_time > NOW() - 10m` | `safe` |
| `current_up_bias` | Bullish Bias Count | Live | Directional mix | Markets currently showing upward pressure | `COUNT(*) WHERE direction_bias='UP'` | `safe` |
| `current_down_bias` | Bearish Bias Count | Live | Directional mix | Markets currently showing downward pressure | `COUNT(*) WHERE direction_bias='DOWN'` | `safe` |
| `avg_live_confidence` | Engine Confidence | Live | Alert reliability | Mean confidence score for active patterns | `AVG(confidence_score)` | `safe` |
| `high_conf_alerts` | Priority Alerts | Live | Top-tier signals | Count of live patterns with 'HIGH' confidence label | `COUNT(*) WHERE confidence_label='HIGH'` | `safe` |

## 6. Similarity and Recognition Stats
| Metric ID | Display Name | Category | Business Purpose | User Facing Definition | Technical Definition | Mode Safety |
|-----------|--------------|----------|------------------|-----------------------|----------------------|-------------|
| `highest_similarity` | Max Match Score | Similarity | Show pattern repetition | The strongest match found against historical data | `MAX(similarity_score)` | `safe` |
| `pattern_library_size` | Pattern Library | Similarity | Scale of memory | Number of unique historical profiles for matching | `COUNT(*) FROM pattern_vectors` | `safe` |
| `avg_nearest_matches` | Avg Match Support | Similarity | Search breadth | Mean number of historical matches found per live alert | `AVG(nearest_match_count)` | `safe` |

## 7. Behavior and Follow-Through (Outcome) Stats
| Metric ID | Display Name | Category | Business Purpose | User Facing Definition | Technical Definition | Mode Safety |
|-----------|--------------|----------|------------------|-----------------------|----------------------|-------------|
| `hold_rate_5m` | 5m Follow-Through | Outcomes | Performance claim (short) | % of patterns that hold their direction for 5 mins | `(COUNT(outcome_5m_pips > 0) / total_turns) * 100` | `live_only` |
| `hold_rate_10m` | 10m Follow-Through | Outcomes | Performance claim (med) | % of patterns that hold their direction for 10 mins | `(COUNT(outcome_10m_pips > 0) / total_turns) * 100` | `live_only` |
| `avg_move_10m` | Avg Return (pips) | Outcomes | Expected move | Mean pip movement 10 mins after pattern confirmation | `AVG(outcome_10m_pips)` | `live_only` |
| `hard_failure_rate` | Reversal Rate | Outcomes | Risk transparency | % of patterns that immediately move against detection | `(COUNT(outcome_5m_pips < 0) / total_turns) * 100` | `live_only` |

## 8. Operational Smoke Stats
| Metric ID | Display Name | Category | Business Purpose | User Facing Definition | Technical Definition | Mode Safety |
|-----------|--------------|----------|------------------|-----------------------|----------------------|-------------|
| `db_latency` | Write Latency | Operational | Monitoring lag | Seconds between market event and DB persistence | `MAX(created_at - snapshot_time)` | `safe` |
| `pipeline_health` | Pipeline Score | Operational | High-level uptime | Combined score of process, data, and writing | `(1 - (missing_buckets/expected_buckets)) * 100` | `safe` |

## Implementation Notes
- **SIM vs LIVE separation**: Statistics must be recalculatable per `market_mode`. 
- **Marketing Bias**: For public landing pages, emphasize **Recognition Accuracy** and **Structural Repetition** over "Pip Profitability" to avoid regulatory/misleading claims if using SIM data.
- **Refresh Cadence**:
  - `Core/Live`: 30 seconds.
  - `Detection/Coverage`: 5 minutes.
  - `Similarity/Library`: 1 hour.
  - `Outcomes`: Daily.
