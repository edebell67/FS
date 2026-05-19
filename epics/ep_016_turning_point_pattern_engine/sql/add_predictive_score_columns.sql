-- Add predictive score columns to live_pattern_windows
-- Date: 2026-05-04
-- Purpose: Store direct feature scoring (r=+0.78) alongside similarity scoring (r=-0.13)

ALTER TABLE live_pattern_windows
    ADD COLUMN IF NOT EXISTS predictive_score NUMERIC(12, 4),
    ADD COLUMN IF NOT EXISTS score_confidence_label TEXT;

COMMENT ON COLUMN live_pattern_windows.predictive_score IS
    'Direct feature score: reversal_strength*5 + cluster_width*4 + magnet_shift_post*3. Correlation r=+0.78 with outcomes.';

COMMENT ON COLUMN live_pattern_windows.score_confidence_label IS
    'Confidence based on predictive_score thresholds (SCORE_HIGH/MEDIUM_HIGH/MEDIUM/LOW).';
