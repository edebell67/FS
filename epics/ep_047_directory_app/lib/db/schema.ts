// lib/db/schema.ts — Drizzle schema for the directory application.
//
// VERSION HISTORY
// v1.2.0 · 2026-08-10 · Adds message_versions, outreach_responses, and
//   commercial_opportunities for the EP043 CRM reporting layer, plus
//   verification_deliveries.message_version_id linking outbound sends to a
//   frozen version. Everything else the CRM reads (businesses,
//   verification_batches/items, pipeline_stages, stage_transitions,
//   verification_deliveries) already existed.
// v1.1.0 · 2026-08-05 · Adds durable hashed owner-review links, decisions, and page responses.
// v1.0.0 · 2026-08-05 · Version history added; file predates this convention.
//
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
  date,
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

    // Preview delivery and review (EP047 preview-delivery-and-review workflow).
    // generatedSiteUrl points at the ep044_group-generated static site once
    // the background watcher has produced it; awaitingOwnerResponseSince
    // drives the intake/review reminder nudges (absence of a submission,
    // not partial view data, is what a reminder fires on).
    generatedSiteUrl: text("generated_site_url"),
    websiteGeneratedAt: timestamp("website_generated_at", { withTimezone: true }),
    // Whether the generated site should wire in the shared AI chat widget
    // (assistant-embed.js's ASSISTANT_ENABLED flag). Defaults to true to match
    // the ep044_group skill's own default-on behaviour.
    chatWidgetOptIn: boolean("chat_widget_opt_in").notNull().default(true),
    awaitingOwnerResponseSince: timestamp("awaiting_owner_response_since", { withTimezone: true }),
    readyForActivationSetAt: timestamp("ready_for_activation_set_at", { withTimezone: true }),
    readyForActivationDate: timestamp("ready_for_activation_date", { withTimezone: true }),
    nextServiceDate: timestamp("next_service_date", { withTimezone: true }),
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

// Claim-approval messages are deliberately separate from the claim decision.
// An approved business is Claimed even if its optional owner notification is
// still prepared or fails delivery; the two states remain visible and auditable.
export const claimSuccessMessages = pgTable(
  "claim_success_messages",
  {
    id: uuid("id").primaryKey().defaultRandom(),
    claimRequestId: uuid("claim_request_id").notNull().unique().references(() => claimRequests.id, { onDelete: "cascade" }),
    businessId: uuid("business_id").notNull().references(() => businesses.id, { onDelete: "cascade" }),
    recipientAddress: text("recipient_address"),
    status: text("status").notNull().default("prepared"), // prepared | sent | failed | not_ready
    subject: text("subject").notNull(),
    textBody: text("text_body").notNull(),
    actorUserId: uuid("actor_user_id").references(() => users.id),
    providerMessageId: text("provider_message_id"),
    failureReason: text("failure_reason"),
    createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
    sentAt: timestamp("sent_at", { withTimezone: true }),
    failedAt: timestamp("failed_at", { withTimezone: true }),
  },
  (table) => ({
    byStatus: index("claim_success_messages_status_idx").on(table.status, table.createdAt),
  })
);

// Preview-ready / ETA / ready-for-activation messages, plus their reminder
// nudges, share one table distinguished by messageType. A reminder is its
// own record, never a resend of the message it nudges — this is what keeps
// "was the owner reminded" answerable without re-deriving it from timestamps.
export const previewDeliveryMessages = pgTable(
  "preview_delivery_messages",
  {
    id: uuid("id").primaryKey().defaultRandom(),
    businessId: uuid("business_id").notNull().references(() => businesses.id, { onDelete: "cascade" }),
    messageType: text("message_type").notNull(),
    // preview_ready | eta | ready_for_activation |
    // reminder_intake | reminder_review | reminder_activation
    recipientAddress: text("recipient_address"),
    status: text("status").notNull().default("prepared"), // prepared | sent | failed
    subject: text("subject").notNull(),
    textBody: text("text_body").notNull(),
    actorUserId: uuid("actor_user_id").references(() => users.id),
    providerMessageId: text("provider_message_id"),
    failureReason: text("failure_reason"),
    createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
    sentAt: timestamp("sent_at", { withTimezone: true }),
    failedAt: timestamp("failed_at", { withTimezone: true }),
  },
  (table) => ({
    byBusinessAndType: index("preview_delivery_messages_business_type_idx")
      .on(table.businessId, table.messageType, table.createdAt),
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
    // Links this send to a frozen MessageVersion row for EP043 CRM
    // reporting (message-version comparison). Nullable because deliveries
    // predating the CRM's message-versioning tables have no version to
    // point at.
    messageVersionId: uuid("message_version_id").references(() => messageVersions.id),
    actorUserId: uuid("actor_user_id").references(() => users.id),
    status: text("status").notNull().default("prepared"),
    deliveryMode: text("delivery_mode").notNull().default("disabled"),
    // SHA-256 only. The raw tracking proof travels in the one-time admin
    // preview and email URLs; it is never persisted.
    trackingKeyHash: text("tracking_key_hash").notNull(),
    createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
    handoffStartedAt: timestamp("handoff_started_at", { withTimezone: true }),
    sentAt: timestamp("sent_at", { withTimezone: true }),
    openedAt: timestamp("opened_at", { withTimezone: true }),
    clickedAt: timestamp("clicked_at", { withTimezone: true }),
    completedAt: timestamp("completed_at", { withTimezone: true }),
    revokedAt: timestamp("revoked_at", { withTimezone: true }),
    failedAt: timestamp("failed_at", { withTimezone: true }),
    providerMessageId: text("provider_message_id"),
    failureReason: text("failure_reason"),
  },
  (table) => ({
    byLink: index("verification_deliveries_link_idx").on(table.verificationLinkId),
    byBatchItem: index("verification_deliveries_batch_item_idx").on(table.batchItemId),
  })
);

// Append-only, non-sensitive lifecycle evidence. Event metadata must never
// contain verification or tracking capabilities.
export const verificationDeliveryEvents = pgTable(
  "verification_delivery_events",
  {
    id: uuid("id").primaryKey().defaultRandom(),
    deliveryId: uuid("delivery_id").notNull()
      .references(() => verificationDeliveries.id, { onDelete: "cascade" }),
    eventType: text("event_type").notNull(),
    actorUserId: uuid("actor_user_id").references(() => users.id),
    metadata: jsonb("metadata").notNull().default({}),
    occurredAt: timestamp("occurred_at", { withTimezone: true }).notNull().defaultNow(),
  },
  (table) => ({
    byDelivery: index("verification_delivery_events_delivery_idx")
      .on(table.deliveryId, table.occurredAt),
  })
);

// --- EP048 consumer lead capture and controlled lead access -----------------
//
// Consumer contact details are stored only in job_leads and are never selected
// for public cards. A business can receive those details only through a paid,
// server-side access grant; the attribution row is append-only business outcome
// evidence, not a reason to expose contact data early.
export const jobLeads = pgTable(
  "job_leads",
  {
    id: uuid("id").primaryKey().defaultRandom(),
    name: text("name").notNull(),
    email: text("email").notNull(),
    phone: text("phone"),
    location: text("location").notNull(),
    tradeRequested: text("trade_requested").notNull(),
    sizeOfWork: text("size_of_work").notNull(),
    budget: doublePrecision("budget").notNull(),
    status: text("status").notNull().default("open"), // open | assigned | completed | withdrawn
    createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
  },
  (table) => ({
    byPublicFeed: index("job_leads_public_feed_idx").on(table.status, table.createdAt),
    byTradeLocation: index("job_leads_trade_location_idx").on(table.tradeRequested, table.location),
  })
);

export const leadAccessGrants = pgTable(
  "lead_access_grants",
  {
    id: uuid("id").primaryKey().defaultRandom(),
    leadId: uuid("lead_id").notNull().references(() => jobLeads.id, { onDelete: "cascade" }),
    businessId: uuid("business_id").notNull().references(() => businesses.id, { onDelete: "cascade" }),
    price: doublePrecision("price").notNull(),
    status: text("status").notNull().default("pending"), // pending | paid | refunded | cancelled
    paymentReference: text("payment_reference"),
    paidAt: timestamp("paid_at", { withTimezone: true }),
    createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
  },
  (table) => ({
    oneBusinessPerLead: uniqueIndex("lead_access_grants_business_lead_uidx").on(table.leadId, table.businessId),
    byBusinessStatus: index("lead_access_grants_business_status_idx").on(table.businessId, table.status),
  })
);

export const leadAttributions = pgTable(
  "lead_attributions",
  {
    id: uuid("id").primaryKey().defaultRandom(),
    leadId: uuid("lead_id").notNull().references(() => jobLeads.id, { onDelete: "cascade" }),
    businessId: uuid("business_id").notNull().references(() => businesses.id, { onDelete: "cascade" }),
    accessGrantId: uuid("access_grant_id").notNull().unique().references(() => leadAccessGrants.id, { onDelete: "restrict" }),
    status: text("status").notNull().default("contacted"), // contacted | quoted | won
    createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
    updatedAt: timestamp("updated_at", { withTimezone: true }).notNull().defaultNow(),
  },
  (table) => ({
    byLead: index("lead_attributions_lead_idx").on(table.leadId, table.createdAt),
    byBusiness: index("lead_attributions_business_idx").on(table.businessId, table.status),
  })
);

// --- CRM: message versioning, response tracking, commercial opportunities --
//
// EP043 CRM reporting layer (workstream/600_workflow/ep043/EP043_crm_business_
// outreach_workflow.html). Business/batch/pipeline/outbound-delivery data
// already exists above (businesses, verification_batches, pipeline_stages,
// stage_transitions, verification_deliveries) — the CRM reads all of that
// read-only. These three tables are what was missing: a frozen/versioned
// message template, a place to record and classify inbound replies, and
// commercial (claim/activation/service revenue) outcomes.

export const messageVersions = pgTable(
  "message_versions",
  {
    id: uuid("id").primaryKey().defaultRandom(),
    templateName: text("template_name").notNull(), // e.g. "claim_listing", "preview_followup"
    versionNumber: integer("version_number").notNull(),
    subject: text("subject").notNull(),
    body: text("body").notNull(),
    campaignRef: text("campaign_ref"),
    dateIntroduced: timestamp("date_introduced", { withTimezone: true }).notNull().defaultNow(),
    dateRetired: timestamp("date_retired", { withTimezone: true }),
    createdByUserId: uuid("created_by_user_id").references(() => users.id),
    createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
  },
  (table) => ({
    // Versions are frozen: a template can have many versions, but never two
    // rows claiming the same version number for the same template name.
    templateVersion: uniqueIndex("message_versions_template_version_uidx").on(table.templateName, table.versionNumber),
    byTemplate: index("message_versions_template_idx").on(table.templateName),
  })
);

export const outreachResponses = pgTable(
  "outreach_responses",
  {
    id: uuid("id").primaryKey().defaultRandom(),
    businessId: uuid("business_id").notNull().references(() => businesses.id, { onDelete: "cascade" }),
    deliveryId: uuid("delivery_id").references(() => verificationDeliveries.id),
    batchItemId: uuid("batch_item_id").references(() => verificationBatchItems.id),
    messageVersionId: uuid("message_version_id").references(() => messageVersions.id),
    channel: text("channel").notNull().default("email"),
    originalBody: text("original_body").notNull(),
    // positive | interested | wants_info | listing_claim_interest |
    // website_interest | follow_up_later | wrong_contact | not_interested |
    // already_has_supplier | no_longer_trading | unsubscribe | other
    classification: text("classification").notNull(),
    receivedAt: timestamp("received_at", { withTimezone: true }).notNull().defaultNow(),
    recordedByUserId: uuid("recorded_by_user_id").references(() => users.id),
    notes: text("notes"),
  },
  (table) => ({
    byBusiness: index("outreach_responses_business_idx").on(table.businessId, table.receivedAt),
    byClassification: index("outreach_responses_classification_idx").on(table.classification, table.receivedAt),
    byMessageVersion: index("outreach_responses_message_version_idx").on(table.messageVersionId),
    byBatchItem: index("outreach_responses_batch_item_idx").on(table.batchItemId),
  })
);

export const commercialOpportunities = pgTable(
  "commercial_opportunities",
  {
    id: uuid("id").primaryKey().defaultRandom(),
    businessId: uuid("business_id").notNull().references(() => businesses.id, { onDelete: "cascade" }).unique(),
    // listing_claimed | preview_sent | preview_viewed | activated | converted
    stage: text("stage").notNull().default("listing_claimed"),
    claimedAt: timestamp("claimed_at", { withTimezone: true }),
    activationValue: doublePrecision("activation_value"),
    activatedAt: timestamp("activated_at", { withTimezone: true }),
    serviceType: text("service_type"),
    serviceValue: doublePrecision("service_value"),
    convertedAt: timestamp("converted_at", { withTimezone: true }),
    createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
    updatedAt: timestamp("updated_at", { withTimezone: true }).notNull().defaultNow(),
  },
  (table) => ({
    byStage: index("commercial_opportunities_stage_idx").on(table.stage),
  })
);

// --- Public directory visibility and hyperlocal news -----------------------
//
// Public scope is a publication control, not a deletion mechanism.  The
// singleton settings row chooses whether every imported value is public or
// whether the explicitly enabled values form the public allow-list.  This
// means that newly imported towns/categories work naturally in "all" mode,
// while a focused launch (for example, Birmingham + hairdressers) can be
// deliberately limited without losing the underlying records.
export const publicDirectorySettings = pgTable("public_directory_settings", {
  id: text("id").primaryKey().default("default"),
  townMode: text("town_mode").notNull().default("all"), // all | selected
  categoryMode: text("category_mode").notNull().default("all"), // all | selected
  updatedByUserId: uuid("updated_by_user_id").references(() => users.id),
  updatedAt: timestamp("updated_at", { withTimezone: true }).notNull().defaultNow(),
});

export const publicTownVisibility = pgTable(
  "public_town_visibility",
  {
    id: uuid("id").primaryKey().defaultRandom(),
    // A lower-case, trimmed key keeps comparisons stable while retaining the
    // original display label used by the directory import.
    townKey: text("town_key").notNull().unique(),
    townLabel: text("town_label").notNull(),
    isEnabled: boolean("is_enabled").notNull().default(true),
    updatedByUserId: uuid("updated_by_user_id").references(() => users.id),
    updatedAt: timestamp("updated_at", { withTimezone: true }).notNull().defaultNow(),
  },
  (table) => ({ byEnabled: index("public_town_visibility_enabled_idx").on(table.isEnabled) })
);

export const publicCategoryVisibility = pgTable(
  "public_category_visibility",
  {
    id: uuid("id").primaryKey().defaultRandom(),
    categoryKey: text("category_key").notNull().unique(),
    categoryLabel: text("category_label").notNull(),
    isEnabled: boolean("is_enabled").notNull().default(true),
    updatedByUserId: uuid("updated_by_user_id").references(() => users.id),
    updatedAt: timestamp("updated_at", { withTimezone: true }).notNull().defaultNow(),
  },
  (table) => ({ byEnabled: index("public_category_visibility_enabled_idx").on(table.isEnabled) })
);

export const publicBusinessVisibility = pgTable("public_business_visibility", {
  id: uuid("id").primaryKey().defaultRandom(),
  businessId: uuid("business_id").notNull().references(() => businesses.id, { onDelete: "cascade" }).unique(),
  decision: text("decision").notNull().default("inherit"), // inherit | show | hide
  reason: text("reason").notNull(),
  updatedByUserId: uuid("updated_by_user_id").references(() => users.id),
  updatedAt: timestamp("updated_at", { withTimezone: true }).notNull().defaultNow(),
});

export const publicVisibilityAudit = pgTable("public_visibility_audit", {
  id: uuid("id").primaryKey().defaultRandom(),
  entityType: text("entity_type").notNull(),
  entityKey: text("entity_key").notNull(),
  action: text("action").notNull(),
  reason: text("reason").notNull(),
  actorUserId: uuid("actor_user_id").references(() => users.id),
  createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
});

// The three editorial fields deliberately mirror the agreed reading model:
// verified reporting, a clearly separate newsroom interpretation, and only
// real attributed business voices.  Responses/moderation will be introduced
// in a later task rather than treating generated opinion as evidence.
export const newsArticles = pgTable(
  "news_articles",
  {
    id: uuid("id").primaryKey().defaultRandom(),
    slug: text("slug").notNull().unique(),
    headline: text("headline").notNull(),
    town: text("town").notNull(),
    sourceName: text("source_name").notNull(),
    sourceUrl: text("source_url").notNull(),
    verifiedUpdate: text("verified_update").notNull(),
    localReading: text("local_reading").notNull(),
    businessVoices: text("business_voices"),
    status: text("status").notNull().default("draft"), // draft | review_required | published | archived
    publishedAt: timestamp("published_at", { withTimezone: true }),
    sourcePublishedAt: timestamp("source_published_at", { withTimezone: true }),
    originalEventDate: date("original_event_date"),
    effectiveStoryDate: date("effective_story_date"),
    effectiveDateKind: text("effective_date_kind"),
    dateProvenance: jsonb("date_provenance").notNull().default({}),
    eventIdentity: text("event_identity"),
    duplicateState: text("duplicate_state").notNull().default("unique"),
    duplicateReason: text("duplicate_reason"),
    createdByUserId: uuid("created_by_user_id").references(() => users.id),
    createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
    updatedAt: timestamp("updated_at", { withTimezone: true }).notNull().defaultNow(),
  },
  (table) => ({
    byTownStatus: index("news_articles_town_status_idx").on(table.town, table.status, table.publishedAt),
    byPublished: index("news_articles_published_idx").on(table.status, table.publishedAt),
  })
);

export const newsArticleCategories = pgTable(
  "news_article_categories",
  {
    id: uuid("id").primaryKey().defaultRandom(),
    articleId: uuid("article_id").notNull().references(() => newsArticles.id, { onDelete: "cascade" }),
    categoryKey: text("category_key").notNull(),
    categoryLabel: text("category_label").notNull(),
    createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
  },
  (table) => ({
    articleCategory: uniqueIndex("news_article_categories_article_category_uidx").on(table.articleId, table.categoryKey),
    byCategory: index("news_article_categories_category_idx").on(table.categoryKey),
  })
);

// Owner review capability submissions are deliberately independent of verification and delivery.
export const ownerReviewLinks = pgTable("owner_review_links", {
  id: uuid("id").primaryKey().defaultRandom(), businessId: uuid("business_id").notNull().references(() => businesses.id, { onDelete: "cascade" }),
  tokenHash: text("token_hash").notNull().unique(), expiresAt: timestamp("expires_at", { withTimezone: true }).notNull(),
  openedAt: timestamp("opened_at", { withTimezone: true }), submittedAt: timestamp("submitted_at", { withTimezone: true }), revokedAt: timestamp("revoked_at", { withTimezone: true }),
  createdByUserId: uuid("created_by_user_id").references(() => users.id), createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
});
export const ownerReviewSubmissions = pgTable("owner_review_submissions", {
  id: uuid("id").primaryKey().defaultRandom(), linkId: uuid("link_id").notNull().unique().references(() => ownerReviewLinks.id),
  businessId: uuid("business_id").notNull().references(() => businesses.id, { onDelete: "cascade" }), decision: text("decision").notNull(), submittedAt: timestamp("submitted_at", { withTimezone: true }).notNull().defaultNow(),
});
export const ownerReviewPageResponses = pgTable("owner_review_page_responses", {
  id: uuid("id").primaryKey().defaultRandom(), submissionId: uuid("submission_id").notNull().references(() => ownerReviewSubmissions.id, { onDelete: "cascade" }),
  pageKey: text("page_key").notNull(), noActionRequired: boolean("no_action_required").notNull().default(true), selections: jsonb("selections").notNull().default([]),
  anythingElse: text("anything_else").notNull().default(""), pageOpenDateTime: timestamp("page_open_date_time", { withTimezone: true }),
}, (table) => ({ onePage: uniqueIndex("owner_review_page_response_uidx").on(table.submissionId, table.pageKey) }));
