# Skill: Turning Point Identification (Epic 016)

This skill provides expert guidance for identifying, validating, and querying market "Tops" and "Bottoms" within the Epic 016 Turning Point Pattern Engine.

## Procedural Guidance

### 1. Definition of a Turning Point
A turning point is a structural peak or trough identified through frequency-magnet shifts and price-rejection behavior.
- **TOP**: A point where price has reached a local peak, frequency magnets have shifted downward, and the zone above the peak has vanished.
- **BOTTOM**: A point where price has reached a local trough, frequency magnets have shifted upward, and the zone below the trough has vanished.

### 2. Validation Criteria (The confirmation logic)
A candidate is only promoted to a "Confirmed Turn" if it meets the following:
- **Confirmation Delay**: The turn must be verified by subsequent price movement (typically 3-5 snapshots).
- **Move into Turn**: A minimum pip move into the point must be detected to ensure it's a significant structural event.
- **Magnet Shift**: The dominant frequency cluster (magnet) must physically move in the expected direction after the peak/trough.

### 3. How to Identify Tops (SQL)
To retrieve validated LIVE tops, use the following join:

```sql
SELECT 
    p.product_code, 
    t.turn_time, 
    t.turn_price, 
    t.confirmation_delay_minutes,
    f.pattern_quality_score
FROM turning_points t
JOIN products p ON p.product_id = t.product_id
JOIN frequency_snapshots s ON s.product_id = t.product_id AND s.snapshot_time = t.turn_time
LEFT JOIN pattern_features f ON f.turn_id = t.turn_id
WHERE s.market_mode = 'LIVE' 
  AND t.turn_type = 'TOP'
ORDER BY t.turn_time DESC;
```

### 4. How to Identify Bottoms (SQL)
To retrieve validated LIVE bottoms:

```sql
SELECT 
    p.product_code, 
    t.turn_time, 
    t.turn_price, 
    t.confirmation_delay_minutes,
    f.pattern_quality_score
FROM turning_points t
JOIN products p ON p.product_id = t.product_id
JOIN frequency_snapshots s ON s.product_id = t.product_id AND s.snapshot_time = t.turn_time
LEFT JOIN pattern_features f ON f.turn_id = t.turn_id
WHERE s.market_mode = 'LIVE' 
  AND t.turn_type = 'BOTTOM'
ORDER BY t.turn_time DESC;
```

### 5. Similarity vs. Dynamics (The "Consensus" Logic)
Identifying a turn is only the first step. To reach a **Consensus** on expected behavior, do not rely solely on "Shape Similarity" (Cosine Similarity on the 294D frequency matrix).

**The Problem**: Two patterns can have >95% shape similarity but opposite dynamics (e.g., one strong reversal, one weak stall).
**The Solution**: Use a weighted approach:
1.  **Find N Similar Tops**: Retrieve the top 5-10 structural matches.
2.  **Observe Outcomes**: Calculate the mean and variance of their `outcome_pips`.
3.  **Consensus Check**: If 80% of similar historical tops moved in the same direction, the current candidate is high-confidence.
4.  **Dynamics Weighting**: Give more weight to the 12 behavioral dimensions (magnet shift speed, rebuild score) over the 294 structural dimensions.

### 6. Automated Identification Tool
Use the built-in generator to produce a fresh JSON summary:
`python epics/ep_016_turning_point_pattern_engine/logic/marketing_stats_generator.py`

## Performance Guardrails
- **Mode Isolation**: ALWAYS filter by `market_mode = 'LIVE'` for production reporting.
- **Reconciliation**: If counts mismatch, check the `frequency_snapshots` table to ensure the `turn_time` exists in the snapshot stream for that product.
