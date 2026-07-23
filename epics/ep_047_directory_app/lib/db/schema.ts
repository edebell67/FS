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
} from "drizzle-orm/pg-core";

export const schemaMigrations = pgTable("schema_migrations", {
  id: serial("id").primaryKey(),
  name: text("name").notNull().unique(),
  appliedAt: timestamp("applied_at", { withTimezone: true }).notNull().defaultNow(),
});

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
