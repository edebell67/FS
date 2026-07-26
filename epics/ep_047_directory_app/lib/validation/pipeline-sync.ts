import { sql, type SQL } from "drizzle-orm";

const VALIDATED_STAGE_KEY = "validated";
export const VALIDATION_STAGE_REASON = "field_validation_completed";

type SqlExecutor = {
  execute(query: SQL): Promise<unknown>;
};

/**
 * Advances a fully validated business without ever regressing a later pipeline
 * stage. The business row lock serialises concurrent validation/revalidation
 * completions, while the fixed reason makes the history entry idempotent.
 *
 * This must be called inside the same transaction that persists the successful
 * validation result.
 */
export async function synchroniseValidatedPipelineStage(
  executor: SqlExecutor,
  businessId: string,
  occurredAt: Date,
): Promise<void> {
  await executor.execute(sql`
    WITH target_stage AS (
      SELECT id, sort_order
      FROM pipeline_stages
      WHERE key = ${VALIDATED_STAGE_KEY}
    ),
    eligible_business AS MATERIALIZED (
      SELECT business.id, business.current_stage_id
      FROM businesses business
      INNER JOIN pipeline_stages current_stage
        ON current_stage.id = business.current_stage_id
      CROSS JOIN target_stage
      WHERE business.id = ${businessId}::uuid
        AND current_stage.sort_order < target_stage.sort_order
      FOR UPDATE OF business
    ),
    transition AS (
      INSERT INTO stage_transitions (
        business_id, from_stage_id, to_stage_id, occurred_at, source, reason
      )
      SELECT eligible.id, eligible.current_stage_id, target.id,
             ${occurredAt}, 'automation', ${VALIDATION_STAGE_REASON}
      FROM eligible_business eligible
      CROSS JOIN target_stage target
      WHERE NOT EXISTS (
        SELECT 1
        FROM stage_transitions existing
        WHERE existing.business_id = eligible.id
          AND existing.to_stage_id = target.id
          AND existing.source = 'automation'
          AND existing.reason = ${VALIDATION_STAGE_REASON}
      )
      ON CONFLICT DO NOTHING
    )
    UPDATE businesses business
    SET current_stage_id = target.id,
        stage_entered_at = ${occurredAt},
        last_updated = ${occurredAt}
    FROM eligible_business eligible
    CROSS JOIN target_stage target
    WHERE business.id = eligible.id
  `);
}
