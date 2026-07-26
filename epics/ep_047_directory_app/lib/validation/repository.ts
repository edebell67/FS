import { randomUUID } from "node:crypto";
import { and, desc, eq, sql } from "drizzle-orm";
import { db } from "@/lib/db/client";
import {
  businesses, businessValidationRuns, fieldRepairHistory, fieldValidationOutcomes,
  validationFieldRules, validationJobItems, validationJobs, validationPolicy,
} from "@/lib/db/schema";
import { validateBusiness } from "./engine";
import { synchroniseValidatedPipelineStage } from "./pipeline-sync";
import {
  RULE_TYPES, VALIDATABLE_FIELDS, type RuleType, type ValidatableField, type ValidationRule,
} from "./types";

export function canManageValidation(role: string): boolean {
  return ["super_admin", "admin", "operations"].includes(role);
}

function asRules(rows: Array<typeof validationFieldRules.$inferSelect>): ValidationRule[] {
  return rows.map((row) => ({
    id: row.id,
    fieldName: row.fieldName as ValidatableField,
    label: row.label,
    ruleType: row.ruleType as RuleType,
    mandatory: row.mandatory,
    blocksVerification: row.blocksVerification,
    parameters: (row.parameters ?? {}) as ValidationRule["parameters"],
  }));
}

export async function listValidationRules() {
  return db.select().from(validationFieldRules)
    .where(eq(validationFieldRules.active, true))
    .orderBy(validationFieldRules.fieldName, validationFieldRules.ruleType);
}

export async function getValidationPolicy() {
  const [policy] = await db.select().from(validationPolicy).where(eq(validationPolicy.id, 1)).limit(1);
  return policy ?? { id: 1, allowPartialVerification: false, updatedByUserId: null, updatedAt: new Date(0) };
}

export async function setPartialVerificationPolicy(allow: boolean, actorUserId: string) {
  await db.insert(validationPolicy).values({
    id: 1, allowPartialVerification: allow, updatedByUserId: actorUserId, updatedAt: new Date(),
  }).onConflictDoUpdate({
    target: validationPolicy.id,
    set: { allowPartialVerification: allow, updatedByUserId: actorUserId, updatedAt: new Date() },
  });
}

export async function replaceValidationRule(input: {
  fieldName: string; label: string; ruleType: string; mandatory: boolean;
  blocksVerification: boolean; pattern?: string; min?: number; max?: number;
}, actorUserId: string) {
  if (!VALIDATABLE_FIELDS.includes(input.fieldName as ValidatableField)) throw new Error("Unsupported field.");
  if (!RULE_TYPES.includes(input.ruleType as RuleType)) throw new Error("Unsupported rule type.");
  if (!input.label.trim()) throw new Error("Rule label is required.");
  if (input.ruleType === "regex") {
    if (!input.pattern) throw new Error("A regex pattern is required.");
    try { new RegExp(input.pattern); } catch { throw new Error("The regex pattern is invalid."); }
  }
  const parameters = input.ruleType === "regex" ? { pattern: input.pattern }
    : input.ruleType === "number_range" ? { min: input.min, max: input.max } : {};
  await db.transaction(async (tx) => {
    await tx.update(validationFieldRules).set({ active: false, supersededAt: new Date() }).where(and(
      eq(validationFieldRules.fieldName, input.fieldName),
      eq(validationFieldRules.ruleType, input.ruleType),
      eq(validationFieldRules.active, true),
    ));
    await tx.insert(validationFieldRules).values({
      fieldName: input.fieldName, label: input.label.trim(), ruleType: input.ruleType,
      mandatory: input.mandatory, blocksVerification: input.blocksVerification,
      parameters, createdByUserId: actorUserId,
    });
  });
}

export async function runBusinessValidation(
  businessId: string, trigger: "import" | "admin" | "repair" | "rules_changed", actorUserId?: string,
  rulesOverride?: ValidationRule[], validationJobItemId?: string,
) {
  return db.transaction(async (tx) => {
    if (validationJobItemId) {
      const [existing] = await tx.select({
        id: businessValidationRuns.id, status: businessValidationRuns.status,
      }).from(businessValidationRuns)
        .where(eq(businessValidationRuns.validationJobItemId, validationJobItemId)).limit(1);
      if (existing) {
        return {
          status: existing.status as "non_valid" | "partially_validated" | "validated",
          outcomes: [], outstandingFields: [], runId: existing.id,
        };
      }
    }
    const [business] = await tx.select().from(businesses).where(eq(businesses.id, businessId)).limit(1);
    if (!business) throw new Error("Business not found.");
    const rules = rulesOverride ?? asRules(
      await tx.select().from(validationFieldRules).where(eq(validationFieldRules.active, true)),
    );
    const result = validateBusiness(business, rules);
    const now = new Date();
    const [run] = await tx.insert(businessValidationRuns).values({
      businessId, status: result.status, trigger, rulesSnapshot: rules,
      actorUserId: actorUserId || null, validationJobItemId: validationJobItemId ?? null,
      startedAt: now, completedAt: now,
    }).returning();
    if (!run) throw new Error("Unable to persist validation run.");
    if (result.outcomes.length) {
      await tx.insert(fieldValidationOutcomes).values(result.outcomes.map((outcome) => ({
        runId: run.id, businessId, ruleId: outcome.ruleId || null, fieldName: outcome.fieldName,
        sourceValue: outcome.sourceValue, normalizedValue: outcome.normalizedValue,
        passed: outcome.passed, outcomeCode: outcome.outcomeCode, message: outcome.message,
        mandatory: outcome.mandatory, blocksVerification: outcome.blocksVerification,
      })));
    }
    await tx.update(businesses).set({
      validationStatus: result.status, lastValidationRunId: run.id,
      validatedAt: result.status === "validated" ? now : null,
    }).where(eq(businesses.id, businessId));
    if (result.status === "validated") {
      await synchroniseValidatedPipelineStage(tx, businessId, now);
    }
    return { ...result, runId: run.id };
  });
}

export const VALIDATION_JOB_CHUNK_SIZE = 25;
const VALIDATION_JOB_LEASE_MINUTES = 5;

export type ValidationJobProgress = {
  id: string;
  status: string;
  totalCount: number;
  processedCount: number;
  errorCount: number;
  createdAt: Date;
  startedAt: Date | null;
  completedAt: Date | null;
  busy: boolean;
  errors: Array<{ businessId: string; message: string }>;
};

export type ValidationStatusSummary = {
  validated: number;
  partiallyValidated: number;
  nonValid: number;
  awaitingValidation: number;
};

export type ValidationOverview = {
  counts: ValidationStatusSummary;
  latestJob: ValidationJobProgress | null;
};

async function validationJobProgress(jobId: string, busy = false): Promise<ValidationJobProgress> {
  const [job] = await db.select().from(validationJobs).where(eq(validationJobs.id, jobId)).limit(1);
  if (!job) throw new Error("Validation run not found.");
  const errors = await db.select({
    businessId: validationJobItems.businessId,
    message: validationJobItems.errorMessage,
  }).from(validationJobItems).where(and(
    eq(validationJobItems.jobId, jobId),
    eq(validationJobItems.status, "failed"),
  )).orderBy(validationJobItems.completedAt).limit(10);
  return {
    id: job.id, status: job.status, totalCount: job.totalCount,
    processedCount: job.processedCount, errorCount: job.errorCount,
    createdAt: job.createdAt, startedAt: job.startedAt, completedAt: job.completedAt,
    busy, errors: errors.map((item) => ({
      businessId: item.businessId, message: item.message ?? "Unknown validation error.",
    })),
  };
}

export async function getLatestValidationJob(): Promise<ValidationJobProgress | null> {
  const [job] = await db.select({ id: validationJobs.id }).from(validationJobs)
    .orderBy(desc(validationJobs.createdAt)).limit(1);
  return job ? validationJobProgress(job.id) : null;
}

export async function getValidationOverview(): Promise<ValidationOverview> {
  const [counts, latestJob] = await Promise.all([
    db.select({
      validated: sql<number>`count(*) FILTER (
        WHERE ${businesses.lastValidationRunId} IS NOT NULL
          AND ${businesses.validationStatus} = 'validated'
      )::int`,
      partiallyValidated: sql<number>`count(*) FILTER (
        WHERE ${businesses.lastValidationRunId} IS NOT NULL
          AND ${businesses.validationStatus} = 'partially_validated'
      )::int`,
      nonValid: sql<number>`count(*) FILTER (
        WHERE ${businesses.lastValidationRunId} IS NOT NULL
          AND ${businesses.validationStatus} = 'non_valid'
      )::int`,
      awaitingValidation: sql<number>`count(*) FILTER (
        WHERE ${businesses.lastValidationRunId} IS NULL
      )::int`,
    }).from(businesses).where(eq(businesses.status, "active")),
    getLatestValidationJob(),
  ]);
  return {
    counts: counts[0] ?? {
      validated: 0, partiallyValidated: 0, nonValid: 0, awaitingValidation: 0,
    },
    latestJob,
  };
}

export async function startBusinessValidationJob(actorUserId: string): Promise<ValidationJobProgress> {
  const jobId = await db.transaction(async (tx) => {
    // Serializes kickoff across application instances; the partial unique
    // index is a second line of defence against more than one active run.
    await tx.execute(sql`SELECT pg_advisory_xact_lock(hashtext('business-validation-job-kickoff'))`);
    const [existing] = await tx.select({ id: validationJobs.id }).from(validationJobs)
      .where(sql`${validationJobs.status} IN ('pending', 'running')`).limit(1);
    if (existing) return existing.id;

    const rules = asRules(
      await tx.select().from(validationFieldRules).where(eq(validationFieldRules.active, true)),
    );
    const [job] = await tx.insert(validationJobs).values({
      status: "pending", rulesSnapshot: rules, createdByUserId: actorUserId,
    }).returning({ id: validationJobs.id });
    if (!job) throw new Error("Unable to create validation run.");

    await tx.execute(sql`
      INSERT INTO validation_job_items (job_id, business_id)
      SELECT ${job.id}::uuid, id FROM businesses WHERE status = 'active'
      ON CONFLICT (job_id, business_id) DO NOTHING
    `);
    const countResult = await tx.execute(sql`
      SELECT count(*)::int AS count FROM validation_job_items WHERE job_id = ${job.id}::uuid
    `);
    const total = Number(countResult.rows[0]?.count ?? 0);
    await tx.update(validationJobs).set({
      totalCount: total,
      status: total === 0 ? "completed" : "pending",
      completedAt: total === 0 ? new Date() : null,
      updatedAt: new Date(),
    }).where(eq(validationJobs.id, job.id));
    return job.id;
  });
  return validationJobProgress(jobId);
}

export async function processBusinessValidationJobChunk(
  jobId: string,
  actorUserId: string,
): Promise<ValidationJobProgress> {
  const claimToken = randomUUID();
  const claimed = await db.transaction(async (tx) => {
    const lockResult = await tx.execute(sql`
      SELECT id, status, rules_snapshot, lease_token, lease_expires_at
      FROM validation_jobs WHERE id = ${jobId}::uuid FOR UPDATE
    `);
    const job = lockResult.rows[0] as {
      status: string; rules_snapshot: ValidationRule[];
      lease_token: string | null; lease_expires_at: Date | string | null;
    } | undefined;
    if (!job) throw new Error("Validation run not found.");
    if (!["pending", "running"].includes(job.status)) return { rules: job.rules_snapshot, ids: [] };

    const leaseExpiresAt = job.lease_expires_at ? new Date(job.lease_expires_at) : null;
    if (job.lease_token && leaseExpiresAt && leaseExpiresAt > new Date()) return null;

    // A crashed request leaves processing items behind. Once its lease has
    // expired, returning them to pending makes the run safely resumable.
    await tx.execute(sql`
      UPDATE validation_job_items
      SET status = 'pending', claim_token = NULL
      WHERE job_id = ${jobId}::uuid AND status = 'processing'
    `);
    const itemResult = await tx.execute(sql`
      WITH next_items AS (
        SELECT id FROM validation_job_items
        WHERE job_id = ${jobId}::uuid AND status = 'pending'
        ORDER BY id
        LIMIT ${VALIDATION_JOB_CHUNK_SIZE}
        FOR UPDATE
      )
      UPDATE validation_job_items item
      SET status = 'processing', claim_token = ${claimToken}::uuid,
          attempt_count = attempt_count + 1, started_at = now(), error_message = NULL
      FROM next_items
      WHERE item.id = next_items.id
      RETURNING item.id, item.business_id
    `);
    await tx.execute(sql`
      UPDATE validation_jobs
      SET status = 'running', started_at = COALESCE(started_at, now()),
          lease_token = ${claimToken}::uuid,
          lease_expires_at = now() + (${VALIDATION_JOB_LEASE_MINUTES} * interval '1 minute'),
          updated_at = now()
      WHERE id = ${jobId}::uuid
    `);
    return {
      rules: job.rules_snapshot,
      ids: itemResult.rows as Array<{ id: string; business_id: string }>,
    };
  });

  if (!claimed) return validationJobProgress(jobId, true);

  for (const item of claimed.ids) {
    try {
      const result = await runBusinessValidation(
        item.business_id, "admin", actorUserId, claimed.rules, item.id,
      );
      await db.update(validationJobItems).set({
        status: "completed", validationRunId: result.runId, completedAt: new Date(),
      }).where(and(
        eq(validationJobItems.id, item.id),
        eq(validationJobItems.claimToken, claimToken),
      ));
    } catch (error) {
      const message = error instanceof Error ? error.message : "Unknown validation error.";
      await db.update(validationJobItems).set({
        status: "failed", errorMessage: message.slice(0, 2000), completedAt: new Date(),
      }).where(and(
        eq(validationJobItems.id, item.id),
        eq(validationJobItems.claimToken, claimToken),
      ));
    }
  }

  await db.transaction(async (tx) => {
    const counts = await tx.execute(sql`
      SELECT
        count(*) FILTER (WHERE status IN ('completed','failed'))::int AS processed,
        count(*) FILTER (WHERE status = 'failed')::int AS errors,
        count(*) FILTER (WHERE status = 'pending')::int AS pending
      FROM validation_job_items WHERE job_id = ${jobId}::uuid
    `);
    const row = counts.rows[0] as { processed: number; errors: number; pending: number };
    const finished = Number(row.pending) === 0;
    await tx.update(validationJobs).set({
      processedCount: Number(row.processed), errorCount: Number(row.errors),
      status: finished ? (Number(row.errors) ? "completed_with_errors" : "completed") : "running",
      completedAt: finished ? new Date() : null,
      leaseToken: null, leaseExpiresAt: null, updatedAt: new Date(),
    }).where(and(eq(validationJobs.id, jobId), eq(validationJobs.leaseToken, claimToken)));
  });
  return validationJobProgress(jobId);
}

export async function getBusinessValidationDetail(businessId: string) {
  const [business] = await db.select({
    id: businesses.id, businessRef: businesses.businessRef, businessName: businesses.businessName,
    validationStatus: businesses.validationStatus, lastValidationRunId: businesses.lastValidationRunId,
  }).from(businesses).where(eq(businesses.id, businessId)).limit(1);
  if (!business) return null;
  const outcomes = business.lastValidationRunId ? await db.select().from(fieldValidationOutcomes)
    .where(eq(fieldValidationOutcomes.runId, business.lastValidationRunId))
    .orderBy(fieldValidationOutcomes.fieldName) : [];
  const repairs = await db.select().from(fieldRepairHistory)
    .where(eq(fieldRepairHistory.businessId, businessId))
    .orderBy(desc(fieldRepairHistory.createdAt));
  return { ...business, outcomes, repairs };
}

export async function listRepairQueue() {
  return db.select({
    outcomeId: fieldValidationOutcomes.id, businessId: businesses.id,
    businessRef: businesses.businessRef, businessName: businesses.businessName,
    fieldName: fieldValidationOutcomes.fieldName, sourceValue: fieldValidationOutcomes.sourceValue,
    message: fieldValidationOutcomes.message, validationStatus: businesses.validationStatus,
  }).from(businesses)
    .innerJoin(fieldValidationOutcomes, and(
      eq(fieldValidationOutcomes.runId, businesses.lastValidationRunId),
      eq(fieldValidationOutcomes.passed, false),
    ))
    .orderBy(fieldValidationOutcomes.fieldName, businesses.businessName);
}

const REPAIRABLE_COLUMNS = {
  businessName: businesses.businessName, tradingName: businesses.tradingName, category: businesses.category,
  subCategory: businesses.subCategory, email: businesses.email, phone: businesses.phone, mobile: businesses.mobile,
  website: businesses.website, facebook: businesses.facebook, instagram: businesses.instagram,
  linkedin: businesses.linkedin, address: businesses.address, town: businesses.town, county: businesses.county,
  postcode: businesses.postcode, description: businesses.description,
} as const;

export async function applyFieldRepair(input: {
  businessId: string; outcomeId: string; fieldName: string; proposedValue: string; evidence: string;
}, actorUserId: string) {
  const column = REPAIRABLE_COLUMNS[input.fieldName as keyof typeof REPAIRABLE_COLUMNS];
  if (!column) throw new Error("This field cannot be repaired through the text repair form.");
  if (!input.evidence.trim()) throw new Error("Repair evidence is required.");
  const [outcome] = await db.select().from(fieldValidationOutcomes).where(and(
    eq(fieldValidationOutcomes.id, input.outcomeId), eq(fieldValidationOutcomes.businessId, input.businessId),
    eq(fieldValidationOutcomes.fieldName, input.fieldName), eq(fieldValidationOutcomes.passed, false),
    sql`${fieldValidationOutcomes.runId} = (
      SELECT last_validation_run_id FROM businesses WHERE id = ${input.businessId}::uuid
    )`,
  )).limit(1);
  if (!outcome) throw new Error("Outstanding field outcome not found.");
  const [repair] = await db.insert(fieldRepairHistory).values({
    businessId: input.businessId, fieldName: input.fieldName, sourceOutcomeId: outcome.id,
    sourceValue: outcome.sourceValue, proposedValue: input.proposedValue, replacementValue: input.proposedValue,
    evidence: input.evidence.trim(), actorUserId, status: "proposed",
  }).returning();
  if (!repair) throw new Error("Unable to persist repair evidence.");
  await db.update(businesses).set({ [input.fieldName]: input.proposedValue, lastUpdated: new Date() })
    .where(eq(businesses.id, input.businessId));
  const result = await runBusinessValidation(input.businessId, "repair", actorUserId);
  await db.update(fieldRepairHistory).set({
    status: "applied", appliedAt: new Date(), revalidationRunId: result.runId,
  }).where(eq(fieldRepairHistory.id, repair.id));
  return result;
}

export async function outstandingFieldsForRun(runId: string | null): Promise<string[]> {
  if (!runId) return [];
  const rows = await db.select({ fieldName: fieldValidationOutcomes.fieldName })
    .from(fieldValidationOutcomes)
    .where(and(eq(fieldValidationOutcomes.runId, runId), eq(fieldValidationOutcomes.passed, false)));
  return [...new Set(rows.map((row) => row.fieldName))];
}
