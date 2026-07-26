-- Keep one durable automation transition for the validation milestone. The
-- predicate leaves unrelated/manual stage history untouched.
CREATE UNIQUE INDEX IF NOT EXISTS stage_transitions_validation_completed_uidx
  ON stage_transitions (business_id, to_stage_id)
  WHERE source = 'automation' AND reason = 'field_validation_completed';
--> statement-breakpoint

-- Backfill only fully validated businesses that are still in Imported.
-- Preserve the actual validation time where available, falling back to the
-- referenced validation run completion time for legacy projections.
WITH imported_stage AS (
  SELECT id FROM pipeline_stages WHERE key = 'imported'
),
validated_stage AS (
  SELECT id FROM pipeline_stages WHERE key = 'validated'
),
eligible AS MATERIALIZED (
  SELECT
    business.id,
    business.current_stage_id,
    COALESCE(
      business.validated_at,
      validation_run.completed_at,
      business.last_updated,
      business.import_date
    ) AS transition_at
  FROM businesses business
  INNER JOIN imported_stage imported
    ON business.current_stage_id = imported.id
  LEFT JOIN business_validation_runs validation_run
    ON validation_run.id = business.last_validation_run_id
  WHERE business.validation_status = 'validated'
  FOR UPDATE OF business
),
inserted_transitions AS (
  INSERT INTO stage_transitions (
    business_id, from_stage_id, to_stage_id, occurred_at, source, reason, notes
  )
  SELECT
    eligible.id,
    eligible.current_stage_id,
    validated.id,
    eligible.transition_at,
    'automation',
    'field_validation_completed',
    'Backfilled from durable field-validation status'
  FROM eligible
  CROSS JOIN validated_stage validated
  WHERE NOT EXISTS (
    SELECT 1
    FROM stage_transitions existing
    WHERE existing.business_id = eligible.id
      AND existing.to_stage_id = validated.id
      AND existing.source = 'automation'
      AND existing.reason = 'field_validation_completed'
  )
  ON CONFLICT DO NOTHING
)
UPDATE businesses business
SET current_stage_id = validated.id,
    stage_entered_at = eligible.transition_at,
    last_updated = GREATEST(business.last_updated, eligible.transition_at)
FROM eligible
CROSS JOIN validated_stage validated
WHERE business.id = eligible.id;
