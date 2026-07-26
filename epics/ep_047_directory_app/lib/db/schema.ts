// Phase 1 (partial) — the slice of the schema needed to import businesses.
//
// This is deliberately a subset of PLAN.md §2, not the full model. It covers
// what CSV/JSON import touches: businesses, the pipeline stage a business
// lands on, the transition that puts it there, and the import batch/error
// bookkeeping that powers rollback and the error report.
//
// Not yet here (still to come as the admin console and analytics phases
// need them): stage_transitions beyond the single import-time row, events,
// audit_log, users/roles, notifications, jobs, metrics_daily. Adding those
// is additive, not a rewrite of what's below.

import {
  pgTable,
  serial,
  text,
  timestamp,
  uuid,
  integer,
  bigint,
  boolean,
  jsonb,
  doublePrecision,
  index,
  uniqueIndex,
} from "drizzle-orm/pg-core";
import { sql } from "drizzle-orm";

export const schemaMigrations = pgTable("schema_migrations", {
  id: serial("id").primaryKey(),
  name: text("name").notNull().unique(),
  appliedAt: timestamp("applied_at", { withTimezone: true }).notNull().defaultNow(),
});

// --- Admin auth -------------------------------------------------------------

// The brief's six roles (Super Admin, Admin, Sales, Operations, Support,
// Read Only) are stored here but NOT yet enforced per-permission — every
// authenticated user currently gets full /directoryadmin access regardless
// of role. Role is recorded now so a later pass can add the permission
// matrix without a schema change. See lib/auth/roles.ts for the fixed list.
export const users = pgTable("users", {
  id: uuid("id").primaryKey().defaultRandom(),
  email: text("email").notNull().unique(),
  // "scrypt$salt$hash" — see lib/auth/password.ts. Never a plain password,
  // never logged, never returned from any query used by the UI.
  passwordHash: text("password_hash").notNull(),
  role: text("role").notNull().default("admin"),
  createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
  lastLoginAt: timestamp("last_login_at", { withTimezone: true }),
});

// Session tokens are random (256 bits), never signed/decoded — the cookie
// value is looked up here by its hash. AUTH_SECRET is NOT used for sessions;
// nothing here depends on it. Deleting a user cascades to their sessions,
// so revoking access is one DELETE.
export const sessions = pgTable(
  "sessions",
  {
    id: uuid("id").primaryKey().defaultRandom(),
    userId: uuid("user_id")
      .notNull()
      .references(() => users.id, { onDelete: "cascade" }),
    // SHA-256 hex of the raw cookie token — the raw token is never stored,
    // so a DB leak alone doesn't hand out usable sessions.
    tokenHash: text("token_hash").notNull().unique(),
    expiresAt: timestamp("expires_at", { withTimezone: true }).notNull(),
    createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
  },
  (table) => ({
    byUser: index("sessions_user_idx").on(table.userId),
    byExpiry: index("sessions_expiry_idx").on(table.expiresAt),
  })
);

// --- Pipeline -------------------------------------------------------------

export const pipelineStages = pgTable("pipeline_stages", {
  id: serial("id").primaryKey(),
  key: text("key").notNull().unique(), // e.g. "imported", "validated"
  label: text("label").notNull(),
  sortOrder: integer("sort_order").notNull(),
  boardColumn: text("board_column").notNull(), // one of the 8 Kanban columns
  isTerminal: boolean("is_terminal").notNull().default(false),
  slaHours: integer("sla_hours"),
});

// --- Import bookkeeping ----------------------------------------------------

export const importBatches = pgTable("import_batches", {
  id: uuid("id").primaryKey().defaultRandom(),
  filename: text("filename").notNull(),
  source: text("source").notNull(), // "csv" | "json" | "api"
  uploadedBy: text("uploaded_by"),
  status: text("status").notNull().default("processing"), // processing | completed | rolled_back | failed
  totalRows: integer("total_rows").notNull().default(0),
  acceptedRows: integer("accepted_rows").notNull().default(0),
  rejectedRows: integer("rejected_rows").notNull().default(0),
  duplicateRows: integer("duplicate_rows").notNull().default(0),
  createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
  completedAt: timestamp("completed_at", { withTimezone: true }),
});

export const importRowErrors = pgTable(
  "import_row_errors",
  {
    id: serial("id").primaryKey(),
    batchId: uuid("batch_id")
      .notNull()
      .references(() => importBatches.id, { onDelete: "cascade" }),
    rowNumber: integer("row_number").notNull(),
    column: text("column"),
    rawValue: text("raw_value"),
    errorCode: text("error_code").notNull(), // e.g. "invalid_email", "missing_field", "duplicate"
    message: text("message").notNull(),
  },
  (table) => ({
    byBatch: index("import_row_errors_batch_idx").on(table.batchId),
  })
);

// Per-category counter backing the immutable business_ref, e.g. TP-PLUMB-000001.
export const categorySequences = pgTable("category_sequences", {
  categoryCode: text("category_code").primaryKey(), // e.g. "PLUMB"
  nextVal: bigint("next_val", { mode: "number" }).notNull().default(1),
});

// --- Businesses -------------------------------------------------------------

export const businesses = pgTable(
  "businesses",
  {
    id: uuid("id").primaryKey().defaultRandom(),

    // Permanent public identifier, e.g. TP-PLUMB-000001. Enforced immutable
    // by a trigger added in the migration SQL (Drizzle can't express
    // "no UPDATE" declaratively).
    businessRef: text("business_ref").notNull().unique(),
    slug: text("slug").notNull().unique(),

    businessName: text("business_name").notNull(),
    tradingName: text("trading_name"),
    category: text("category").notNull(),
    subCategory: text("sub_category"),

    email: text("email"),
    phone: text("phone"),
    mobile: text("mobile"),
    website: text("website"),
    facebook: text("facebook"),
    instagram: text("instagram"),
    linkedin: text("linkedin"),

    address: text("address"),
    town: text("town"),
    county: text("county"),
    postcode: text("postcode"),
    latitude: doublePrecision("latitude"),
    longitude: doublePrecision("longitude"),
    // location geography(Point,4326) lands alongside PostGIS setup —
    // generated from latitude/longitude in the migration SQL, not modelled
    // in Drizzle's TS schema.

    googleRating: doublePrecision("google_rating"),
    reviewCount: integer("review_count"),
    openingHours: jsonb("opening_hours"),
    description: text("description"),

    importedSource: text("imported_source").notNull(), // "csv" | "json" | "api"
    importBatchId: uuid("import_batch_id").references(() => importBatches.id),
    importDate: timestamp("import_date", { withTimezone: true }).notNull().defaultNow(),
    lastUpdated: timestamp("last_updated", { withTimezone: true }).notNull().defaultNow(),

    status: text("status").notNull().default("active"), // active | claimed | published | cancelled | archived
    currentStageId: integer("current_stage_id").references(() => pipelineStages.id),
    stageEnteredAt: timestamp("stage_entered_at", { withTimezone: true }),

    notes: text("notes"),
    internalNotes: text("internal_notes"),
    tags: text("tags").array(),
    validationStatus: text("validation_status").notNull().default("non_valid"),
    lastValidationRunId: uuid("last_validation_run_id"),
    validatedAt: timestamp("validated_at", { withTimezone: true }),
  },
  (table) => ({
    byCategory: index("businesses_category_idx").on(table.category),
    byTown: index("businesses_town_idx").on(table.town),
    byCounty: index("businesses_county_idx").on(table.county),
    // Not unique: duplicate detection combines email/phone/website/name+postcode
    // (see lib/import/duplicates.ts) — no single field is an absolute identity key.
    byEmail: index("businesses_email_idx").on(table.email),
    byStage: index("businesses_stage_idx").on(table.currentStageId),
  })
);

// Data-quality rules are versioned by replacement/deactivation. Validation
// runs and their field outcomes are immutable evidence; businesses carries
// only the latest projection used for filtering and batch eligibility.
export const validationFieldRules = pgTable(
  "validation_field_rules",
  {
    id: uuid("id").primaryKey().defaultRandom(),
    fieldName: text("field_name").notNull(),
    label: text("label").notNull(),
    ruleType: text("rule_type").notNull(),
    mandatory: boolean("mandatory").notNull().default(false),
    blocksVerification: boolean("blocks_verification").notNull().default(false),
    parameters: jsonb("parameters").notNull().default({}),
    active: boolean("active").notNull().default(true),
    createdByUserId: uuid("created_by_user_id").references(() => users.id),
    createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
    supersededAt: timestamp("superseded_at", { withTimezone: true }),
  },
  (table) => ({
    activeFieldRule: uniqueIndex("validation_field_rules_active_uidx")
      .on(table.fieldName, table.ruleType)
      .where(sql`${table.active} = true`),
  })
);

export const businessValidationRuns = pgTable(
  "business_validation_runs",
  {
    id: uuid("id").primaryKey().defaultRandom(),
    businessId: uuid("business_id").notNull().references(() => businesses.id, { onDelete: "cascade" }),
    status: text("status").notNull(),
    trigger: text("trigger").notNull(),
    rulesSnapshot: jsonb("rules_snapshot").notNull(),
    actorUserId: uuid("actor_user_id").references(() => users.id),
    // Idempotency key for durable bulk work. It intentionally has no FK here
    // because the job-item table is declared later in this schema.
    validationJobItemId: uuid("validation_job_item_id").unique(),
    startedAt: timestamp("started_at", { withTimezone: true }).notNull().defaultNow(),
    completedAt: timestamp("completed_at", { withTimezone: true }).notNull().defaultNow(),
  },
  (table) => ({ byBusiness: index("business_validation_runs_business_idx").on(table.businessId, table.completedAt) })
);

export const fieldValidationOutcomes = pgTable(
  "field_validation_outcomes",
  {
    id: uuid("id").primaryKey().defaultRandom(),
    runId: uuid("run_id").notNull().references(() => businessValidationRuns.id, { onDelete: "cascade" }),
    // Keep the snapshot even if the business is deleted mid-run; processing
    // then records a visible "Business not found" error instead of losing count.
    businessId: uuid("business_id").notNull(),
    ruleId: uuid("rule_id").references(() => validationFieldRules.id),
    fieldName: text("field_name").notNull(),
    sourceValue: text("source_value"),
    normalizedValue: text("normalized_value"),
    passed: boolean("passed").notNull(),
    outcomeCode: text("outcome_code").notNull(),
    message: text("message"),
    mandatory: boolean("mandatory").notNull(),
    blocksVerification: boolean("blocks_verification").notNull(),
    createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
  },
  (table) => ({
    byBusinessRun: index("field_validation_outcomes_business_run_idx").on(table.businessId, table.runId),
    repairQueue: index("field_validation_outcomes_repair_idx").on(table.fieldName, table.passed),
  })
);

export const fieldRepairHistory = pgTable(
  "field_repair_history",
  {
    id: uuid("id").primaryKey().defaultRandom(),
    businessId: uuid("business_id").notNull().references(() => businesses.id, { onDelete: "cascade" }),
    fieldName: text("field_name").notNull(),
    sourceOutcomeId: uuid("source_outcome_id").notNull().references(() => fieldValidationOutcomes.id),
    sourceValue: text("source_value"),
    proposedValue: text("proposed_value").notNull(),
    replacementValue: text("replacement_value"),
    evidence: text("evidence").notNull(),
    actorUserId: uuid("actor_user_id").notNull().references(() => users.id),
    status: text("status").notNull().default("proposed"),
    revalidationRunId: uuid("revalidation_run_id").references(() => businessValidationRuns.id),
    createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
    appliedAt: timestamp("applied_at", { withTimezone: true }),
  },
  (table) => ({ byBusiness: index("field_repair_history_business_idx").on(table.businessId, table.createdAt) })
);

export const validationPolicy = pgTable("validation_policy", {
  id: integer("id").primaryKey().default(1),
  allowPartialVerification: boolean("allow_partial_verification").notNull().default(false),
  updatedByUserId: uuid("updated_by_user_id").references(() => users.id),
  updatedAt: timestamp("updated_at", { withTimezone: true }).notNull().defaultNow(),
});

// Durable orchestration for validating the active-business population. The
// per-business tables remain the immutable evidence; these rows only track
// bounded, resumable bulk work.
export const validationJobs = pgTable(
  "validation_jobs",
  {
    id: uuid("id").primaryKey().defaultRandom(),
    status: text("status").notNull().default("pending"),
    totalCount: integer("total_count").notNull().default(0),
    processedCount: integer("processed_count").notNull().default(0),
    errorCount: integer("error_count").notNull().default(0),
    rulesSnapshot: jsonb("rules_snapshot").notNull(),
    createdByUserId: uuid("created_by_user_id").notNull().references(() => users.id),
    leaseToken: uuid("lease_token"),
    leaseExpiresAt: timestamp("lease_expires_at", { withTimezone: true }),
    createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
    startedAt: timestamp("started_at", { withTimezone: true }),
    completedAt: timestamp("completed_at", { withTimezone: true }),
    updatedAt: timestamp("updated_at", { withTimezone: true }).notNull().defaultNow(),
  },
  (table) => ({
    byCreatedAt: index("validation_jobs_created_idx").on(table.createdAt),
    oneActiveJob: uniqueIndex("validation_jobs_one_active_uidx")
      .on(sql`(true)`)
      .where(sql`${table.status} IN ('pending', 'running')`),
  })
);

export const validationJobItems = pgTable(
  "validation_job_items",
  {
    id: uuid("id").primaryKey().defaultRandom(),
    jobId: uuid("job_id").notNull().references(() => validationJobs.id, { onDelete: "cascade" }),
    businessId: uuid("business_id").notNull().references(() => businesses.id, { onDelete: "cascade" }),
    status: text("status").notNull().default("pending"),
    attemptCount: integer("attempt_count").notNull().default(0),
    claimToken: uuid("claim_token"),
    validationRunId: uuid("validation_run_id").references(() => businessValidationRuns.id, { onDelete: "set null" }),
    errorMessage: text("error_message"),
    startedAt: timestamp("started_at", { withTimezone: true }),
    completedAt: timestamp("completed_at", { withTimezone: true }),
  },
  (table) => ({
    byJobStatus: index("validation_job_items_job_status_idx").on(table.jobId, table.status),
    oneBusinessPerJob: uniqueIndex("validation_job_items_business_uidx").on(table.jobId, table.businessId),
  })
);

// One row per stage change. Append-only — nothing here is ever updated or
// deleted; businesses.currentStageId/stageEnteredAt is the projection,
// written in the same transaction as the row that creates it.
export const stageTransitions = pgTable(
  "stage_transitions",
  {
    id: serial("id").primaryKey(),
    businessId: uuid("business_id")
      .notNull()
      .references(() => businesses.id, { onDelete: "cascade" }),
    fromStageId: integer("from_stage_id").references(() => pipelineStages.id),
    toStageId: integer("to_stage_id")
      .notNull()
      .references(() => pipelineStages.id),
    occurredAt: timestamp("occurred_at", { withTimezone: true }).notNull().defaultNow(),
    actorUserId: text("actor_user_id"),
    source: text("source").notNull(), // "import" | "admin" | "api" | "automation" | "owner"
    reason: text("reason"),
    notes: text("notes"),
  },
  (table) => ({
    byBusiness: index("stage_transitions_business_idx").on(table.businessId, table.occurredAt),
    byStage: index("stage_transitions_stage_idx").on(table.toStageId, table.occurredAt),
  })
);

// Owner verification is intentionally separate from businesses.status. Capability
// tokens are stored only as SHA-256 hashes and recipient submissions are snapshots.
export const verificationLinks = pgTable(
  "verification_links",
  {
    id: uuid("id").primaryKey().defaultRandom(),
    businessId: uuid("business_id").notNull().references(() => businesses.id, { onDelete: "cascade" }),
    tokenHash: text("token_hash").notNull(),
    expiresAt: timestamp("expires_at", { withTimezone: true }).notNull(),
    expiresInDays: integer("expires_in_days").notNull().default(5),
    openedAt: timestamp("opened_at", { withTimezone: true }),
    submittedAt: timestamp("submitted_at", { withTimezone: true }),
    revokedAt: timestamp("revoked_at", { withTimezone: true }),
    createdByUserId: uuid("created_by_user_id").references(() => users.id),
    createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
    validationStatusAtIssue: text("validation_status_at_issue"),
    validationRunId: uuid("validation_run_id").references(() => businessValidationRuns.id),
    outstandingFields: jsonb("outstanding_fields").notNull().default([]),
  },
  (table) => ({
    token: uniqueIndex("verification_links_token_hash_uidx").on(table.tokenHash),
    byBusiness: index("verification_links_business_idx").on(table.businessId, table.createdAt),
  })
);

export const verificationBatches = pgTable(
  "verification_batches",
  {
    id: uuid("id").primaryKey().defaultRandom(),
    status: text("status").notNull().default("prepared"),
    expiresInDays: integer("expires_in_days").notNull().default(5),
    totalCount: integer("total_count").notNull(),
    readyCount: integer("ready_count").notNull().default(0),
    createdByUserId: uuid("created_by_user_id").notNull().references(() => users.id),
    createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
  },
  (table) => ({ byCreatedAt: index("verification_batches_created_idx").on(table.createdAt) })
);

export const verificationBatchItems = pgTable(
  "verification_batch_items",
  {
    id: uuid("id").primaryKey().defaultRandom(),
    batchId: uuid("batch_id").notNull().references(() => verificationBatches.id, { onDelete: "cascade" }),
    businessId: uuid("business_id").notNull().references(() => businesses.id, { onDelete: "restrict" }),
    verificationLinkId: uuid("verification_link_id").notNull().unique().references(() => verificationLinks.id),
    recipientChannel: text("recipient_channel").notNull().default("email"),
    recipientAddress: text("recipient_address"),
    status: text("status").notNull().default("prepared"),
    readiness: text("readiness").notNull(),
    readinessReason: text("readiness_reason"),
    createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
  },
  (table) => ({
    byBatch: index("verification_batch_items_batch_idx").on(table.batchId, table.createdAt),
    oneBusinessPerBatch: uniqueIndex("verification_batch_items_business_uidx").on(table.batchId, table.businessId),
  })
);

export const verificationSubmissions = pgTable(
  "verification_submissions",
  {
    id: uuid("id").primaryKey().defaultRandom(),
    linkId: uuid("link_id").notNull().unique().references(() => verificationLinks.id),
    businessId: uuid("business_id").notNull().references(() => businesses.id, { onDelete: "cascade" }),
    submittedFields: jsonb("submitted_fields").notNull(),
    relationshipToBusiness: text("relationship_to_business").notNull(),
    accuracyConfirmedAt: timestamp("accuracy_confirmed_at", { withTimezone: true }).notNull(),
    privacyNoticeVersion: text("privacy_notice_version").notNull(),
    requesterEmail: text("requester_email"),
    requesterPhone: text("requester_phone"),
    submittedAt: timestamp("submitted_at", { withTimezone: true }).notNull().defaultNow(),
  },
  (table) => ({ byBusiness: index("verification_submissions_business_idx").on(table.businessId) })
);

export const claimRequests = pgTable(
  "claim_requests",
  {
    id: uuid("id").primaryKey().defaultRandom(),
    businessId: uuid("business_id").notNull().references(() => businesses.id, { onDelete: "cascade" }),
    submissionId: uuid("submission_id").unique().references(() => verificationSubmissions.id),
    status: text("status").notNull().default("pending"),
    requesterName: text("requester_name").notNull(),
    relationship: text("relationship").notNull(),
    contactEmail: text("contact_email"),
    contactPhone: text("contact_phone"),
    contactFingerprint: text("contact_fingerprint"),
    reviewerUserId: uuid("reviewer_user_id").references(() => users.id),
    reviewedAt: timestamp("reviewed_at", { withTimezone: true }),
    decisionNote: text("decision_note"),
    createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
    updatedAt: timestamp("updated_at", { withTimezone: true }).notNull().defaultNow(),
  },
  (table) => ({
    byBusiness: index("claim_requests_business_idx").on(table.businessId, table.status),
    byContact: index("claim_requests_contact_idx").on(table.contactFingerprint, table.createdAt),
  })
);

export const verificationDeliveries = pgTable(
  "verification_deliveries",
  {
    id: uuid("id").primaryKey().defaultRandom(),
    claimRequestId: uuid("claim_request_id").references(() => claimRequests.id),
    verificationLinkId: uuid("verification_link_id").notNull().references(() => verificationLinks.id),
    batchItemId: uuid("batch_item_id").references(() => verificationBatchItems.id),
    channel: text("channel").notNull().default("email"),
    recipientAddress: text("recipient_address").notNull(),
    templateVersion: text("template_version").notNull(),
    actorUserId: uuid("actor_user_id").references(() => users.id),
    status: text("status").notNull().default("prepared"),
    deliveryMode: text("delivery_mode").notNull().default("disabled"),
    createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
    sentAt: timestamp("sent_at", { withTimezone: true }),
    failedAt: timestamp("failed_at", { withTimezone: true }),
    providerMessageId: text("provider_message_id"),
    failureReason: text("failure_reason"),
  },
  (table) => ({
    byLink: index("verification_deliveries_link_idx").on(table.verificationLinkId),
    byBatchItem: index("verification_deliveries_batch_item_idx").on(table.batchItemId),
  })
);
