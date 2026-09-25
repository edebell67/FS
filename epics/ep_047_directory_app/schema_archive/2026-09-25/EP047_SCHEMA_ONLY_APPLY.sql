-- EP047 code-derived schema-only bundle.
-- Generated from the local source tree on 2026-09-25.
-- NOT an export from ep047-directory-db and contains no row data.
-- Review against a live database inventory before execution.
-- This bundle intentionally excludes INSERT, UPDATE, DELETE, COPY and other DML.
-- Run only against an empty, approved PostgreSQL target; use a transaction and inspect the result.


-- BEGIN migration 0000_init (0000_init.sql)
CREATE TABLE "businesses" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"business_ref" text NOT NULL,
	"slug" text NOT NULL,
	"business_name" text NOT NULL,
	"trading_name" text,
	"category" text NOT NULL,
	"sub_category" text,
	"email" text,
	"phone" text,
	"mobile" text,
	"website" text,
	"facebook" text,
	"instagram" text,
	"linkedin" text,
	"address" text,
	"town" text,
	"county" text,
	"postcode" text,
	"latitude" double precision,
	"longitude" double precision,
	"google_rating" double precision,
	"review_count" integer,
	"opening_hours" jsonb,
	"description" text,
	"imported_source" text NOT NULL,
	"import_batch_id" uuid,
	"import_date" timestamp with time zone DEFAULT now() NOT NULL,
	"last_updated" timestamp with time zone DEFAULT now() NOT NULL,
	"status" text DEFAULT 'active' NOT NULL,
	"current_stage_id" integer,
	"stage_entered_at" timestamp with time zone,
	"notes" text,
	"internal_notes" text,
	"tags" text[],
	CONSTRAINT "businesses_business_ref_unique" UNIQUE("business_ref"),
	CONSTRAINT "businesses_slug_unique" UNIQUE("slug")
);
--> statement-breakpoint
CREATE TABLE "category_sequences" (
	"category_code" text PRIMARY KEY NOT NULL,
	"next_val" bigint DEFAULT 1 NOT NULL
);
--> statement-breakpoint
CREATE TABLE "import_batches" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"filename" text NOT NULL,
	"source" text NOT NULL,
	"uploaded_by" text,
	"status" text DEFAULT 'processing' NOT NULL,
	"total_rows" integer DEFAULT 0 NOT NULL,
	"accepted_rows" integer DEFAULT 0 NOT NULL,
	"rejected_rows" integer DEFAULT 0 NOT NULL,
	"duplicate_rows" integer DEFAULT 0 NOT NULL,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	"completed_at" timestamp with time zone
);
--> statement-breakpoint
CREATE TABLE "import_row_errors" (
	"id" serial PRIMARY KEY NOT NULL,
	"batch_id" uuid NOT NULL,
	"row_number" integer NOT NULL,
	"column" text,
	"raw_value" text,
	"error_code" text NOT NULL,
	"message" text NOT NULL
);
--> statement-breakpoint
CREATE TABLE "pipeline_stages" (
	"id" serial PRIMARY KEY NOT NULL,
	"key" text NOT NULL,
	"label" text NOT NULL,
	"sort_order" integer NOT NULL,
	"board_column" text NOT NULL,
	"is_terminal" boolean DEFAULT false NOT NULL,
	"sla_hours" integer,
	CONSTRAINT "pipeline_stages_key_unique" UNIQUE("key")
);
--> statement-breakpoint
CREATE TABLE "schema_migrations" (
	"id" serial PRIMARY KEY NOT NULL,
	"name" text NOT NULL,
	"applied_at" timestamp with time zone DEFAULT now() NOT NULL,
	CONSTRAINT "schema_migrations_name_unique" UNIQUE("name")
);
--> statement-breakpoint
CREATE TABLE "stage_transitions" (
	"id" serial PRIMARY KEY NOT NULL,
	"business_id" uuid NOT NULL,
	"from_stage_id" integer,
	"to_stage_id" integer NOT NULL,
	"occurred_at" timestamp with time zone DEFAULT now() NOT NULL,
	"actor_user_id" text,
	"source" text NOT NULL,
	"reason" text,
	"notes" text
);
--> statement-breakpoint
ALTER TABLE "businesses" ADD CONSTRAINT "businesses_import_batch_id_import_batches_id_fk" FOREIGN KEY ("import_batch_id") REFERENCES "public"."import_batches"("id") ON DELETE no action ON UPDATE no action;
--> statement-breakpoint
ALTER TABLE "businesses" ADD CONSTRAINT "businesses_current_stage_id_pipeline_stages_id_fk" FOREIGN KEY ("current_stage_id") REFERENCES "public"."pipeline_stages"("id") ON DELETE no action ON UPDATE no action;
--> statement-breakpoint
ALTER TABLE "import_row_errors" ADD CONSTRAINT "import_row_errors_batch_id_import_batches_id_fk" FOREIGN KEY ("batch_id") REFERENCES "public"."import_batches"("id") ON DELETE cascade ON UPDATE no action;
--> statement-breakpoint
ALTER TABLE "stage_transitions" ADD CONSTRAINT "stage_transitions_business_id_businesses_id_fk" FOREIGN KEY ("business_id") REFERENCES "public"."businesses"("id") ON DELETE cascade ON UPDATE no action;
--> statement-breakpoint
ALTER TABLE "stage_transitions" ADD CONSTRAINT "stage_transitions_from_stage_id_pipeline_stages_id_fk" FOREIGN KEY ("from_stage_id") REFERENCES "public"."pipeline_stages"("id") ON DELETE no action ON UPDATE no action;
--> statement-breakpoint
ALTER TABLE "stage_transitions" ADD CONSTRAINT "stage_transitions_to_stage_id_pipeline_stages_id_fk" FOREIGN KEY ("to_stage_id") REFERENCES "public"."pipeline_stages"("id") ON DELETE no action ON UPDATE no action;
--> statement-breakpoint
CREATE INDEX "businesses_category_idx" ON "businesses" USING btree ("category");
--> statement-breakpoint
CREATE INDEX "businesses_town_idx" ON "businesses" USING btree ("town");
--> statement-breakpoint
CREATE INDEX "businesses_county_idx" ON "businesses" USING btree ("county");
--> statement-breakpoint
CREATE INDEX "businesses_email_idx" ON "businesses" USING btree ("email");
--> statement-breakpoint
CREATE INDEX "businesses_stage_idx" ON "businesses" USING btree ("current_stage_id");
--> statement-breakpoint
CREATE INDEX "import_row_errors_batch_idx" ON "import_row_errors" USING btree ("batch_id");
--> statement-breakpoint
CREATE INDEX "stage_transitions_business_idx" ON "stage_transitions" USING btree ("business_id","occurred_at");
--> statement-breakpoint
CREATE INDEX "stage_transitions_stage_idx" ON "stage_transitions" USING btree ("to_stage_id","occurred_at");
-- END migration 0000_init

-- BEGIN migration 0001_pipeline_seed (0001_pipeline_seed.sql)
-- Hand-written follow-up to 0000_init.sql: the two things Drizzle's
-- declarative schema can't express — an immutability trigger and seed data.

-- business_ref is permanent per PLAN.md §2 ("never changes"). Drizzle has no
-- concept of "no UPDATE on this column", so it's enforced here.
CREATE OR REPLACE FUNCTION prevent_business_ref_update()
RETURNS trigger AS $$
BEGIN
  IF NEW.business_ref IS DISTINCT FROM OLD.business_ref THEN
    RAISE EXCEPTION 'business_ref is immutable and cannot be changed (was %, attempted %)',
      OLD.business_ref, NEW.business_ref;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
--> statement-breakpoint

DROP TRIGGER IF EXISTS businesses_business_ref_immutable ON businesses;
--> statement-breakpoint

CREATE TRIGGER businesses_business_ref_immutable
BEFORE UPDATE ON businesses
FOR EACH ROW
EXECUTE FUNCTION prevent_business_ref_update();
--> statement-breakpoint

-- The 22 default pipeline stages from PLAN.md §2 / PROJECT_PROMPT.md.
-- board_column buckets them into the 8 Kanban columns from the brief's
-- Pipeline Dashboard: Discovered, Imported, Validated, Verification,
-- Claimed, Website, Published, Subscriber. Two judgment calls worth
-- flagging: "Directory Published" (stage 5) rolls into the Validated
-- column, since the board's own "Published" column tracks the *website*
-- going live (stage 15 onward) per the brief's Business Timeline example;
-- EXCLUDED non-DDL or review-required statement:
-- -- Cancelled/Archived are terminal and parked in the Subscriber column as
-- -- exit states rather than getting a ninth column.
-- INSERT INTO pipeline_stages (key, label, sort_order, board_column, is_terminal, sla_hours) VALUES
--   ('discovered',                 'Discovered',                  1,  'Discovered',   false, 72),
--   ('imported',                   'Imported',                    2,  'Imported',     false, 24),
--   ('validated',                  'Validated',                   3,  'Validated',    false, 24),
--   ('categorised',                'Categorised',                 4,  'Validated',    false, 24),
--   ('directory_published',        'Directory Published',         5,  'Validated',    false, NULL),
--   ('verification_email_pending', 'Verification Email Pending',  6,  'Verification', false, 24),
--   ('verification_sent',          'Verification Sent',           7,  'Verification', false, 72),
--   ('verification_opened',        'Verification Opened',         8,  'Verification', false, 168),
--   ('verification_completed',     'Verification Completed',      9,  'Verification', false, NULL),
--   ('business_claimed',           'Business Claimed',            10, 'Claimed',      false, NULL),
--   ('website_generated',          'Website Generated',           11, 'Website',      false, 24),
--   ('website_viewed',             'Website Viewed',              12, 'Website',      false, 168),
--   ('website_ready',              'Website Ready',               13, 'Website',      false, NULL),
--   ('publish_requested',          'Publish Requested',           14, 'Website',      false, 48),
--   ('website_published',          'Website Published',           15, 'Published',    false, NULL),
--   ('ai_assistant_available',     'AI Assistant Available',      16, 'Published',    false, NULL),
--   ('ai_assistant_activated',     'AI Assistant Activated',      17, 'Published',    false, NULL),
--   ('lead_received',              'Lead Received',                18, 'Published',    false, 24),
--   ('customer_contacted',         'Customer Contacted',          19, 'Published',    false, 48),
--   ('subscriber',                 'Subscriber',                  20, 'Subscriber',   true,  NULL),
--   ('cancelled',                  'Cancelled',                   21, 'Subscriber',   true,  NULL),
--   ('archived',                   'Archived',                    22, 'Subscriber',   true,  NULL)
-- ON CONFLICT (key) DO NOTHING;
-- END migration 0001_pipeline_seed

-- BEGIN migration 0002_acoustic_jackpot (0002_acoustic_jackpot.sql)
CREATE TABLE "sessions" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"user_id" uuid NOT NULL,
	"token_hash" text NOT NULL,
	"expires_at" timestamp with time zone NOT NULL,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	CONSTRAINT "sessions_token_hash_unique" UNIQUE("token_hash")
);
--> statement-breakpoint
CREATE TABLE "users" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"email" text NOT NULL,
	"password_hash" text NOT NULL,
	"role" text DEFAULT 'admin' NOT NULL,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	"last_login_at" timestamp with time zone,
	CONSTRAINT "users_email_unique" UNIQUE("email")
);
--> statement-breakpoint
ALTER TABLE "sessions" ADD CONSTRAINT "sessions_user_id_users_id_fk" FOREIGN KEY ("user_id") REFERENCES "public"."users"("id") ON DELETE cascade ON UPDATE no action;
--> statement-breakpoint
CREATE INDEX "sessions_user_idx" ON "sessions" USING btree ("user_id");
--> statement-breakpoint
CREATE INDEX "sessions_expiry_idx" ON "sessions" USING btree ("expires_at");
-- END migration 0002_acoustic_jackpot

-- BEGIN migration 0003_business_verification (0003_business_verification.sql)
CREATE TABLE IF NOT EXISTS verification_links (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  business_id uuid NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
  token_hash text NOT NULL UNIQUE,
  expires_at timestamptz NOT NULL,
  expires_in_days integer NOT NULL DEFAULT 5 CHECK (expires_in_days BETWEEN 1 AND 14),
  opened_at timestamptz, submitted_at timestamptz, revoked_at timestamptz,
  created_by_user_id uuid REFERENCES users(id),
  created_at timestamptz NOT NULL DEFAULT now()
);
--> statement-breakpoint
CREATE INDEX IF NOT EXISTS verification_links_business_idx ON verification_links(business_id, created_at);
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS verification_submissions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  link_id uuid NOT NULL UNIQUE REFERENCES verification_links(id),
  business_id uuid NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
  submitted_fields jsonb NOT NULL,
  relationship_to_business text NOT NULL,
  accuracy_confirmed_at timestamptz NOT NULL,
  privacy_notice_version text NOT NULL,
  requester_email text, requester_phone text,
  submitted_at timestamptz NOT NULL DEFAULT now()
);
--> statement-breakpoint
CREATE INDEX IF NOT EXISTS verification_submissions_business_idx ON verification_submissions(business_id);
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS claim_requests (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  business_id uuid NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
  submission_id uuid UNIQUE REFERENCES verification_submissions(id),
  status text NOT NULL DEFAULT 'pending' CHECK (status IN ('pending_contact_verification','pending','approved','declined','withdrawn')),
  requester_name text NOT NULL,
  relationship text NOT NULL,
  contact_email text, contact_phone text, contact_fingerprint text,
  reviewer_user_id uuid REFERENCES users(id), reviewed_at timestamptz, decision_note text,
  created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now()
);
--> statement-breakpoint
CREATE INDEX IF NOT EXISTS claim_requests_business_idx ON claim_requests(business_id, status);
--> statement-breakpoint
CREATE INDEX IF NOT EXISTS claim_requests_contact_idx ON claim_requests(contact_fingerprint, created_at);
--> statement-breakpoint
CREATE UNIQUE INDEX IF NOT EXISTS claim_requests_one_active_submission_idx
  ON claim_requests(submission_id) WHERE submission_id IS NOT NULL AND status IN ('pending','approved');
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS verification_deliveries (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  claim_request_id uuid REFERENCES claim_requests(id),
  verification_link_id uuid NOT NULL REFERENCES verification_links(id),
  channel text NOT NULL DEFAULT 'email', recipient_address text NOT NULL,
  template_version text NOT NULL, actor_user_id uuid REFERENCES users(id),
  created_at timestamptz NOT NULL DEFAULT now(), sent_at timestamptz, failed_at timestamptz,
  provider_message_id text, failure_reason text
);
--> statement-breakpoint
CREATE INDEX IF NOT EXISTS verification_deliveries_link_idx ON verification_deliveries(verification_link_id);
-- END migration 0003_business_verification

-- BEGIN migration 0004_verification_batches (0004_verification_batches.sql)
CREATE TABLE IF NOT EXISTS verification_batches (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  status text NOT NULL DEFAULT 'prepared' CHECK (status IN ('prepared','partially_ready','ready','cancelled')),
  expires_in_days integer NOT NULL DEFAULT 5 CHECK (expires_in_days BETWEEN 1 AND 14),
  total_count integer NOT NULL CHECK (total_count > 0),
  ready_count integer NOT NULL DEFAULT 0 CHECK (ready_count >= 0 AND ready_count <= total_count),
  created_by_user_id uuid NOT NULL REFERENCES users(id),
  created_at timestamptz NOT NULL DEFAULT now()
);
--> statement-breakpoint
CREATE INDEX IF NOT EXISTS verification_batches_created_idx ON verification_batches(created_at);
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS verification_batch_items (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  batch_id uuid NOT NULL REFERENCES verification_batches(id) ON DELETE CASCADE,
  business_id uuid NOT NULL REFERENCES businesses(id) ON DELETE RESTRICT,
  verification_link_id uuid NOT NULL UNIQUE REFERENCES verification_links(id),
  recipient_channel text NOT NULL DEFAULT 'email' CHECK (recipient_channel = 'email'),
  recipient_address text,
  status text NOT NULL DEFAULT 'prepared' CHECK (status IN ('prepared','sent','failed','cancelled')),
  readiness text NOT NULL CHECK (readiness IN ('ready','not_ready')),
  readiness_reason text,
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE(batch_id, business_id)
);
--> statement-breakpoint
CREATE INDEX IF NOT EXISTS verification_batch_items_batch_idx ON verification_batch_items(batch_id, created_at);
--> statement-breakpoint
ALTER TABLE verification_deliveries
  ADD COLUMN IF NOT EXISTS batch_item_id uuid REFERENCES verification_batch_items(id),
  ADD COLUMN IF NOT EXISTS status text NOT NULL DEFAULT 'prepared',
  ADD COLUMN IF NOT EXISTS delivery_mode text NOT NULL DEFAULT 'disabled';
--> statement-breakpoint
CREATE INDEX IF NOT EXISTS verification_deliveries_batch_item_idx ON verification_deliveries(batch_item_id);
-- END migration 0004_verification_batches

-- BEGIN migration 0005_field_validation (0005_field_validation.sql)
ALTER TABLE businesses
  ADD COLUMN IF NOT EXISTS validation_status text NOT NULL DEFAULT 'non_valid'
    CHECK (validation_status IN ('non_valid','partially_validated','validated')),
  ADD COLUMN IF NOT EXISTS last_validation_run_id uuid,
  ADD COLUMN IF NOT EXISTS validated_at timestamptz;
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS validation_field_rules (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  field_name text NOT NULL,
  label text NOT NULL,
  rule_type text NOT NULL CHECK (rule_type IN ('presence','email','phone','url','regex','number_range')),
  mandatory boolean NOT NULL DEFAULT false,
  blocks_verification boolean NOT NULL DEFAULT false,
  parameters jsonb NOT NULL DEFAULT '{}'::jsonb,
  active boolean NOT NULL DEFAULT true,
  created_by_user_id uuid REFERENCES users(id),
  created_at timestamptz NOT NULL DEFAULT now(),
  superseded_at timestamptz
);
--> statement-breakpoint
CREATE UNIQUE INDEX IF NOT EXISTS validation_field_rules_active_uidx
  ON validation_field_rules(field_name, rule_type) WHERE active = true;
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS business_validation_runs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  business_id uuid NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
  status text NOT NULL CHECK (status IN ('non_valid','partially_validated','validated')),
  trigger text NOT NULL CHECK (trigger IN ('import','admin','repair','rules_changed')),
  rules_snapshot jsonb NOT NULL,
  actor_user_id uuid REFERENCES users(id),
  started_at timestamptz NOT NULL DEFAULT now(),
  completed_at timestamptz NOT NULL DEFAULT now()
);
--> statement-breakpoint
CREATE INDEX IF NOT EXISTS business_validation_runs_business_idx
  ON business_validation_runs(business_id, completed_at DESC);
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS field_validation_outcomes (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  run_id uuid NOT NULL REFERENCES business_validation_runs(id) ON DELETE CASCADE,
  business_id uuid NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
  rule_id uuid REFERENCES validation_field_rules(id),
  field_name text NOT NULL,
  source_value text,
  normalized_value text,
  passed boolean NOT NULL,
  outcome_code text NOT NULL CHECK (outcome_code IN ('passed','missing','invalid_format','out_of_range')),
  message text,
  mandatory boolean NOT NULL,
  blocks_verification boolean NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now()
);
--> statement-breakpoint
CREATE INDEX IF NOT EXISTS field_validation_outcomes_business_run_idx
  ON field_validation_outcomes(business_id, run_id);
--> statement-breakpoint
CREATE INDEX IF NOT EXISTS field_validation_outcomes_repair_idx
  ON field_validation_outcomes(field_name, passed);
--> statement-breakpoint
ALTER TABLE businesses ADD CONSTRAINT businesses_last_validation_run_fk
  FOREIGN KEY (last_validation_run_id) REFERENCES business_validation_runs(id);
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS field_repair_history (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  business_id uuid NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
  field_name text NOT NULL,
  source_outcome_id uuid NOT NULL REFERENCES field_validation_outcomes(id),
  source_value text,
  proposed_value text NOT NULL,
  replacement_value text,
  evidence text NOT NULL,
  actor_user_id uuid NOT NULL REFERENCES users(id),
  status text NOT NULL DEFAULT 'proposed' CHECK (status IN ('proposed','applied','rejected')),
  revalidation_run_id uuid REFERENCES business_validation_runs(id),
  created_at timestamptz NOT NULL DEFAULT now(),
  applied_at timestamptz
);
--> statement-breakpoint
CREATE INDEX IF NOT EXISTS field_repair_history_business_idx
  ON field_repair_history(business_id, created_at DESC);
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS validation_policy (
  id integer PRIMARY KEY DEFAULT 1 CHECK (id = 1),
  allow_partial_verification boolean NOT NULL DEFAULT false,
  updated_by_user_id uuid REFERENCES users(id),
  updated_at timestamptz NOT NULL DEFAULT now()
);
-- EXCLUDED non-DDL or review-required statement:
-- --> statement-breakpoint
-- INSERT INTO validation_policy(id, allow_partial_verification) VALUES (1, false)
--   ON CONFLICT (id) DO NOTHING;
-- EXCLUDED non-DDL or review-required statement:
-- --> statement-breakpoint
-- INSERT INTO validation_field_rules(field_name, label, rule_type, mandatory, blocks_verification)
-- VALUES
--   ('businessName', 'Business name', 'presence', true, true),
--   ('category', 'Category', 'presence', true, true),
--   ('email', 'Email', 'email', false, false),
--   ('phone', 'Phone', 'phone', false, false),
--   ('website', 'Website', 'url', false, false)
-- ON CONFLICT DO NOTHING;
--> statement-breakpoint
ALTER TABLE verification_links
  ADD COLUMN IF NOT EXISTS validation_status_at_issue text,
  ADD COLUMN IF NOT EXISTS validation_run_id uuid REFERENCES business_validation_runs(id),
  ADD COLUMN IF NOT EXISTS outstanding_fields jsonb NOT NULL DEFAULT '[]'::jsonb;
-- END migration 0005_field_validation

-- BEGIN migration 0006_validation_jobs (0006_validation_jobs.sql)
CREATE TABLE IF NOT EXISTS validation_jobs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  status text NOT NULL DEFAULT 'pending'
    CHECK (status IN ('pending','running','completed','completed_with_errors')),
  total_count integer NOT NULL DEFAULT 0 CHECK (total_count >= 0),
  processed_count integer NOT NULL DEFAULT 0 CHECK (processed_count >= 0),
  error_count integer NOT NULL DEFAULT 0 CHECK (error_count >= 0),
  rules_snapshot jsonb NOT NULL,
  created_by_user_id uuid NOT NULL REFERENCES users(id),
  lease_token uuid,
  lease_expires_at timestamptz,
  created_at timestamptz NOT NULL DEFAULT now(),
  started_at timestamptz,
  completed_at timestamptz,
  updated_at timestamptz NOT NULL DEFAULT now()
);
--> statement-breakpoint
ALTER TABLE business_validation_runs
  ADD COLUMN IF NOT EXISTS validation_job_item_id uuid UNIQUE;
--> statement-breakpoint
CREATE INDEX IF NOT EXISTS validation_jobs_created_idx
  ON validation_jobs(created_at DESC);
--> statement-breakpoint
CREATE UNIQUE INDEX IF NOT EXISTS validation_jobs_one_active_uidx
  ON validation_jobs ((true)) WHERE status IN ('pending','running');
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS validation_job_items (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  job_id uuid NOT NULL REFERENCES validation_jobs(id) ON DELETE CASCADE,
  business_id uuid NOT NULL,
  status text NOT NULL DEFAULT 'pending'
    CHECK (status IN ('pending','processing','completed','failed')),
  attempt_count integer NOT NULL DEFAULT 0 CHECK (attempt_count >= 0),
  claim_token uuid,
  validation_run_id uuid REFERENCES business_validation_runs(id) ON DELETE SET NULL,
  error_message text,
  started_at timestamptz,
  completed_at timestamptz,
  UNIQUE (job_id, business_id)
);
--> statement-breakpoint
CREATE INDEX IF NOT EXISTS validation_job_items_job_status_idx
  ON validation_job_items(job_id, status);
-- END migration 0006_validation_jobs

-- BEGIN migration 0007_validation_pipeline_sync (0007_validation_pipeline_sync.sql)
-- Keep one durable automation transition for the validation milestone. The
-- predicate leaves unrelated/manual stage history untouched.
CREATE UNIQUE INDEX IF NOT EXISTS stage_transitions_validation_completed_uidx
  ON stage_transitions (business_id, to_stage_id)
  WHERE source = 'automation' AND reason = 'field_validation_completed';
-- EXCLUDED non-DDL or review-required statement:
-- --> statement-breakpoint
--
-- -- Backfill only fully validated businesses that are still in Imported.
-- -- Preserve the actual validation time where available, falling back to the
-- -- referenced validation run completion time for legacy projections.
-- WITH imported_stage AS (
--   SELECT id FROM pipeline_stages WHERE key = 'imported'
-- ),
-- validated_stage AS (
--   SELECT id FROM pipeline_stages WHERE key = 'validated'
-- ),
-- eligible AS MATERIALIZED (
--   SELECT
--     business.id,
--     business.current_stage_id,
--     COALESCE(
--       business.validated_at,
--       validation_run.completed_at,
--       business.last_updated,
--       business.import_date
--     ) AS transition_at
--   FROM businesses business
--   INNER JOIN imported_stage imported
--     ON business.current_stage_id = imported.id
--   LEFT JOIN business_validation_runs validation_run
--     ON validation_run.id = business.last_validation_run_id
--   WHERE business.validation_status = 'validated'
--   FOR UPDATE OF business
-- ),
-- inserted_transitions AS (
--   INSERT INTO stage_transitions (
--     business_id, from_stage_id, to_stage_id, occurred_at, source, reason, notes
--   )
--   SELECT
--     eligible.id,
--     eligible.current_stage_id,
--     validated.id,
--     eligible.transition_at,
--     'automation',
--     'field_validation_completed',
--     'Backfilled from durable field-validation status'
--   FROM eligible
--   CROSS JOIN validated_stage validated
--   WHERE NOT EXISTS (
--     SELECT 1
--     FROM stage_transitions existing
--     WHERE existing.business_id = eligible.id
--       AND existing.to_stage_id = validated.id
--       AND existing.source = 'automation'
--       AND existing.reason = 'field_validation_completed'
--   )
--   ON CONFLICT DO NOTHING
-- )
-- UPDATE businesses business
-- SET current_stage_id = validated.id,
--     stage_entered_at = eligible.transition_at,
--     last_updated = GREATEST(business.last_updated, eligible.transition_at)
-- FROM eligible
-- CROSS JOIN validated_stage validated
-- WHERE business.id = eligible.id;
-- END migration 0007_validation_pipeline_sync

-- BEGIN migration 0008_verification_email_delivery (0008_verification_email_delivery.sql)
ALTER TABLE verification_deliveries
  ADD COLUMN IF NOT EXISTS status text NOT NULL DEFAULT 'prepared',
  ADD COLUMN IF NOT EXISTS delivery_mode text NOT NULL DEFAULT 'disabled',
  ADD COLUMN IF NOT EXISTS tracking_key_hash text,
  ADD COLUMN IF NOT EXISTS handoff_started_at timestamptz,
  ADD COLUMN IF NOT EXISTS opened_at timestamptz,
  ADD COLUMN IF NOT EXISTS clicked_at timestamptz,
  ADD COLUMN IF NOT EXISTS completed_at timestamptz,
  ADD COLUMN IF NOT EXISTS revoked_at timestamptz;
-- EXCLUDED non-DDL or review-required statement:
-- --> statement-breakpoint
-- UPDATE verification_deliveries
-- SET tracking_key_hash =
--   md5(id::text || clock_timestamp()::text) ||
--   md5(clock_timestamp()::text || id::text)
-- WHERE tracking_key_hash IS NULL;
--> statement-breakpoint
ALTER TABLE verification_deliveries
  ALTER COLUMN tracking_key_hash SET NOT NULL;
--> statement-breakpoint
ALTER TABLE verification_deliveries
  ADD CONSTRAINT verification_deliveries_status_check
  CHECK (status IN ('prepared','sent','opened','clicked','completed','failed','revoked'));
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS verification_delivery_events (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  delivery_id uuid NOT NULL REFERENCES verification_deliveries(id) ON DELETE CASCADE,
  event_type text NOT NULL CHECK (event_type IN ('prepared','sent','opened','clicked','completed','failed','revoked')),
  actor_user_id uuid REFERENCES users(id),
  metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
  occurred_at timestamptz NOT NULL DEFAULT now()
);
--> statement-breakpoint
CREATE INDEX IF NOT EXISTS verification_delivery_events_delivery_idx
  ON verification_delivery_events(delivery_id, occurred_at);
-- END migration 0008_verification_email_delivery

-- BEGIN migration 0009_repair_verification_delivery_tracking (0009_repair_verification_delivery_tracking.sql)
-- Forward repair for deployments where migration 0008 was recorded without
-- adding delivery-tracking columns. This is intentionally additive and
-- idempotent: the business-detail delivery audit must render for both
-- pre-existing and newly created deliveries.
ALTER TABLE verification_deliveries
  ADD COLUMN IF NOT EXISTS status text NOT NULL DEFAULT 'prepared',
  ADD COLUMN IF NOT EXISTS delivery_mode text NOT NULL DEFAULT 'disabled',
  ADD COLUMN IF NOT EXISTS tracking_key_hash text,
  ADD COLUMN IF NOT EXISTS handoff_started_at timestamptz,
  ADD COLUMN IF NOT EXISTS opened_at timestamptz,
  ADD COLUMN IF NOT EXISTS clicked_at timestamptz,
  ADD COLUMN IF NOT EXISTS completed_at timestamptz,
  ADD COLUMN IF NOT EXISTS revoked_at timestamptz;
-- END migration 0009_repair_verification_delivery_tracking

-- BEGIN migration 0010_apply_delivery_tracking_schema (0010_apply_delivery_tracking_schema.sql)
-- EXCLUDED non-DDL or review-required statement:
-- -- High-water-mark forward repair. Earlier delivery-tracking migration entries
-- -- were recorded before their schema was present in production;
-- EXCLUDED non-DDL or review-required statement:
-- this entry is
-- -- deliberately newer than every existing journal timestamp so Drizzle applies
-- -- it to that database.
-- ALTER TABLE verification_deliveries
--   ADD COLUMN IF NOT EXISTS tracking_key_hash text,
--   ADD COLUMN IF NOT EXISTS handoff_started_at timestamptz,
--   ADD COLUMN IF NOT EXISTS opened_at timestamptz,
--   ADD COLUMN IF NOT EXISTS clicked_at timestamptz,
--   ADD COLUMN IF NOT EXISTS completed_at timestamptz,
--   ADD COLUMN IF NOT EXISTS revoked_at timestamptz;
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS verification_delivery_events (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  delivery_id uuid NOT NULL REFERENCES verification_deliveries(id) ON DELETE CASCADE,
  event_type text NOT NULL CHECK (event_type IN ('prepared','sent','opened','clicked','completed','failed','revoked')),
  actor_user_id uuid REFERENCES users(id),
  metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
  occurred_at timestamptz NOT NULL DEFAULT now()
);
--> statement-breakpoint
CREATE INDEX IF NOT EXISTS verification_delivery_events_delivery_idx
  ON verification_delivery_events(delivery_id, occurred_at);
-- END migration 0010_apply_delivery_tracking_schema

-- BEGIN migration 0011_claims_pending_bulk_approval (0011_claims_pending_bulk_approval.sql)
CREATE TABLE IF NOT EXISTS claim_success_messages (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  claim_request_id uuid NOT NULL UNIQUE REFERENCES claim_requests(id) ON DELETE CASCADE,
  business_id uuid NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
  recipient_address text,
  status text NOT NULL DEFAULT 'prepared' CHECK (status IN ('prepared','sent','failed','not_ready')),
  subject text NOT NULL,
  text_body text NOT NULL,
  actor_user_id uuid REFERENCES users(id),
  provider_message_id text,
  failure_reason text,
  created_at timestamptz NOT NULL DEFAULT now(),
  sent_at timestamptz,
  failed_at timestamptz
);
--> statement-breakpoint
CREATE INDEX IF NOT EXISTS claim_success_messages_status_idx
  ON claim_success_messages(status, created_at);
--> statement-breakpoint
CREATE INDEX IF NOT EXISTS claim_requests_pending_review_idx
  ON claim_requests(created_at)
  WHERE status IN ('pending','pending_contact_verification');
-- END migration 0011_claims_pending_bulk_approval

-- BEGIN migration 0012_backfill_claim_contact_email (0012_backfill_claim_contact_email.sql)
-- EXCLUDED non-DDL or review-required statement:
-- -- Backfill the supplied listing email for pending verification-origin claims
-- -- where the optional preferred-contact field was left blank.
-- UPDATE claim_requests AS claim
-- SET contact_email = NULLIF(BTRIM(submission.submitted_fields->>'email'), '')
-- FROM verification_submissions AS submission
-- WHERE claim.submission_id = submission.id
--   AND claim.status = 'pending'
--   AND claim.contact_email IS NULL
--   AND NULLIF(BTRIM(submission.submitted_fields->>'email'), '') IS NOT NULL;
-- END migration 0012_backfill_claim_contact_email

-- BEGIN migration 0013_public_visibility_and_news_storage (0013_public_visibility_and_news_storage.sql)
-- EXCLUDED non-DDL or review-required statement:
-- -- EP047: Public launch scope and database-backed hyperlocal news.
-- -- These tables are deliberately additive. Visibility controls public output;
-- they do not delete imported business rows or editorial records.

CREATE TABLE IF NOT EXISTS public_directory_settings (
  id text PRIMARY KEY DEFAULT 'default' CHECK (id = 'default'),
  town_mode text NOT NULL DEFAULT 'all' CHECK (town_mode IN ('all', 'selected')),
  category_mode text NOT NULL DEFAULT 'all' CHECK (category_mode IN ('all', 'selected')),
  updated_by_user_id uuid REFERENCES users(id),
  updated_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS public_town_visibility (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  town_key text NOT NULL UNIQUE,
  town_label text NOT NULL,
  is_enabled boolean NOT NULL DEFAULT true,
  updated_by_user_id uuid REFERENCES users(id),
  updated_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS public_town_visibility_enabled_idx ON public_town_visibility(is_enabled);
CREATE TABLE IF NOT EXISTS public_category_visibility (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  category_key text NOT NULL UNIQUE,
  category_label text NOT NULL,
  is_enabled boolean NOT NULL DEFAULT true,
  updated_by_user_id uuid REFERENCES users(id),
  updated_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS public_category_visibility_enabled_idx ON public_category_visibility(is_enabled);
CREATE TABLE IF NOT EXISTS news_articles (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  slug text NOT NULL UNIQUE,
  headline text NOT NULL,
  town text NOT NULL,
  source_name text NOT NULL,
  source_url text NOT NULL,
  verified_update text NOT NULL,
  local_reading text NOT NULL,
  business_voices text,
  status text NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'published', 'archived')),
  published_at timestamptz,
  created_by_user_id uuid REFERENCES users(id),
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS news_articles_town_status_idx ON news_articles(town, status, published_at);
CREATE INDEX IF NOT EXISTS news_articles_published_idx ON news_articles(status, published_at);
CREATE TABLE IF NOT EXISTS news_article_categories (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  article_id uuid NOT NULL REFERENCES news_articles(id) ON DELETE CASCADE,
  category_key text NOT NULL,
  category_label text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT news_article_categories_article_category_uidx UNIQUE(article_id, category_key)
);
CREATE INDEX IF NOT EXISTS news_article_categories_category_idx ON news_article_categories(category_key);
-- END migration 0013_public_visibility_and_news_storage

-- BEGIN migration 0014_preview_delivery_and_review (0014_preview_delivery_and_review.sql)
-- migrations/0014_preview_delivery_and_review.sql — businesses columns and the
-- message table backing the preview-delivery-and-review workflow.
--
-- VERSION HISTORY
-- v1.0.0 · 2026-07-29 · Initial version: 6 additive businesses columns (generated
--   site URL, generation timestamp, reminder/ETA timestamps, next service date)
--   plus preview_delivery_messages, one table keyed by message_type so reminders
--   are their own records rather than resends of the message they nudge.

-- EP047: Preview delivery and review workflow (schema step only, payment
-- excluded as a self-contained follow-up unit per its own workflow doc).
-- Additive only: no existing column is altered or dropped.

ALTER TABLE businesses
  ADD COLUMN IF NOT EXISTS generated_site_url text,
  ADD COLUMN IF NOT EXISTS website_generated_at timestamptz,
  ADD COLUMN IF NOT EXISTS awaiting_owner_response_since timestamptz,
  ADD COLUMN IF NOT EXISTS ready_for_activation_set_at timestamptz,
  ADD COLUMN IF NOT EXISTS ready_for_activation_date timestamptz,
  ADD COLUMN IF NOT EXISTS next_service_date timestamptz;
CREATE TABLE IF NOT EXISTS preview_delivery_messages (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  business_id uuid NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
  message_type text NOT NULL CHECK (message_type IN (
    'preview_ready', 'eta', 'ready_for_activation',
    'reminder_intake', 'reminder_review', 'reminder_activation'
  )),
  recipient_address text,
  status text NOT NULL DEFAULT 'prepared' CHECK (status IN ('prepared', 'sent', 'failed')),
  subject text NOT NULL,
  text_body text NOT NULL,
  actor_user_id uuid REFERENCES users(id),
  provider_message_id text,
  failure_reason text,
  created_at timestamptz NOT NULL DEFAULT now(),
  sent_at timestamptz,
  failed_at timestamptz
);
CREATE INDEX IF NOT EXISTS preview_delivery_messages_business_type_idx
  ON preview_delivery_messages (business_id, message_type, created_at);
-- END migration 0014_preview_delivery_and_review

-- BEGIN migration 0015_public_visibility_overrides_and_audit (0015_public_visibility_overrides_and_audit.sql)
-- EP047: reversible per-listing exceptions and an operator audit trail.
CREATE TABLE IF NOT EXISTS public_business_visibility (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  business_id uuid NOT NULL UNIQUE REFERENCES businesses(id) ON DELETE CASCADE,
  decision text NOT NULL DEFAULT 'inherit' CHECK (decision IN ('inherit','show','hide')),
  reason text NOT NULL,
  updated_by_user_id uuid REFERENCES users(id),
  updated_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS public_visibility_audit (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  entity_type text NOT NULL,
  entity_key text NOT NULL,
  action text NOT NULL,
  reason text NOT NULL,
  actor_user_id uuid REFERENCES users(id),
  created_at timestamptz NOT NULL DEFAULT now()
);
-- END migration 0015_public_visibility_overrides_and_audit

-- BEGIN migration 0016_site_generation_queue_stage (0016_site_generation_queue_stage.sql)
-- EXCLUDED non-DDL or review-required statement:
-- -- migrations/0016_site_generation_queue_stage.sql — adds the generation queue
-- -- stage and renames the post-generation stage to ready_for_preview.
-- --
-- -- VERSION HISTORY
-- -- v1.0.0 · 2026-07-29 · Initial version: inserts awaiting_site_generation at
-- --   sort_order 11 (shifting later stages down) and renames website_generated to
-- --   ready_for_preview, so the pipeline stage itself is the queue signal rather
-- --   than a stage plus a null-column check.
--
-- -- EP047: introduces an explicit queue stage between Claimed and site
-- -- generation being usable, and renames the post-generation stage to match
-- -- the agreed terminology (ready_for_preview). Additive/rename only -- no
-- -- stage is removed, no business row's history is altered beyond the stage
-- -- label/key rename, which is purely presentational.
--
-- -- Make room at sort_order 11 for the new stage.
-- UPDATE pipeline_stages SET sort_order = sort_order + 1 WHERE sort_order >= 11;
--
-- INSERT INTO pipeline_stages (key, label, sort_order, board_column, is_terminal, sla_hours) VALUES
--   ('awaiting_site_generation', 'Awaiting Site Generation', 11, 'Website', false, 24)
-- ON CONFLICT (key) DO NOTHING;
--
-- -- The stage previously called "Website Generated" is the same event as what
-- -- the agreed design now calls "ready_for_preview": generation is complete
-- -- and the business is ready for the preview-ready notification.
-- UPDATE pipeline_stages
-- SET key = 'ready_for_preview', label = 'Ready for Preview'
-- WHERE key = 'website_generated';
-- END migration 0016_site_generation_queue_stage

-- BEGIN migration 0017_chat_widget_opt_in (0017_chat_widget_opt_in.sql)
-- migrations/0017_chat_widget_opt_in.sql — adds the per-business opt-in flag
-- for the shared AI chat widget that every ep044_group generated site wires
-- in by default.
--
-- VERSION HISTORY
-- v1.0.0 · 2026-07-30 · Initial version: additive boolean column, defaults to
--   true to match the skill's own default (assistant-embed.js ships on by
--   default with a single ASSISTANT_ENABLED flag) — this column is what the
--   generation loop reads to decide that flag's value per business, not a
--   new decision the owner has to make before generation can run.

ALTER TABLE businesses ADD COLUMN IF NOT EXISTS chat_widget_opt_in boolean NOT NULL DEFAULT true;
-- END migration 0017_chat_widget_opt_in

-- BEGIN migration 0018_public_news_date_display_rules (0018_public_news_date_display_rules.sql)
-- EP047-2026.08.01.1 — public News date/display rules foundation
-- Adds provenance without rewriting existing published records.
ALTER TABLE news_articles ADD COLUMN IF NOT EXISTS source_published_at timestamptz;
ALTER TABLE news_articles ADD COLUMN IF NOT EXISTS original_event_date date;
ALTER TABLE news_articles ADD COLUMN IF NOT EXISTS effective_story_date date;
ALTER TABLE news_articles ADD COLUMN IF NOT EXISTS effective_date_kind text;
ALTER TABLE news_articles ADD COLUMN IF NOT EXISTS date_provenance jsonb NOT NULL DEFAULT '{}'::jsonb;
ALTER TABLE news_articles ADD COLUMN IF NOT EXISTS event_identity text;
ALTER TABLE news_articles ADD COLUMN IF NOT EXISTS duplicate_state text NOT NULL DEFAULT 'unique';
ALTER TABLE news_articles ADD COLUMN IF NOT EXISTS duplicate_reason text;
CREATE TABLE IF NOT EXISTS public_news_display_settings (
  id boolean PRIMARY KEY DEFAULT true,
  max_articles_per_town integer NOT NULL DEFAULT 10 CHECK (max_articles_per_town BETWEEN 1 AND 100),
  lookback_days integer NOT NULL DEFAULT 30 CHECK (lookback_days BETWEEN 1 AND 3650),
  status text NOT NULL DEFAULT 'published',
  updated_by_user_id uuid REFERENCES users(id),
  updated_at timestamptz NOT NULL DEFAULT now()
);
-- EXCLUDED non-DDL or review-required statement:
-- INSERT INTO public_news_display_settings (id) VALUES (true) ON CONFLICT (id) DO NOTHING;
CREATE INDEX IF NOT EXISTS news_articles_effective_public_idx
  ON news_articles (status, town, effective_story_date DESC, published_at DESC);
CREATE INDEX IF NOT EXISTS news_articles_event_identity_idx
  ON news_articles (event_identity) WHERE event_identity IS NOT NULL;
-- END migration 0018_public_news_date_display_rules

-- BEGIN migration 0019_news_intake_batch_ledger (0019_news_intake_batch_ledger.sql)
-- EXCLUDED non-DDL or review-required statement:
-- -- EP047-2026.08.02.1 — Durable private News JSON intake ledger.
-- -- Additive only. Imported content is always held as draft or review_required;
-- publication remains a separately authorised editorial action.
CREATE TABLE IF NOT EXISTS news_intake_batches (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  batch_key text NOT NULL UNIQUE,
  schema_version text NOT NULL,
  source_filename text NOT NULL,
  content_hash text NOT NULL,
  status text NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'completed', 'completed_with_rejections', 'retryable', 'failed')),
  attempt_count integer NOT NULL DEFAULT 0 CHECK (attempt_count BETWEEN 0 AND 3),
  next_retry_at timestamptz,
  last_error text,
  started_at timestamptz,
  completed_at timestamptz,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS news_intake_items (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  batch_id uuid NOT NULL REFERENCES news_intake_batches(id) ON DELETE CASCADE,
  item_key text NOT NULL,
  content_hash text NOT NULL,
  status text NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'draft', 'review_required', 'rejected', 'retryable', 'failed', 'duplicate')),
  article_id uuid REFERENCES news_articles(id),
  attempt_count integer NOT NULL DEFAULT 0 CHECK (attempt_count BETWEEN 0 AND 3),
  audit jsonb NOT NULL DEFAULT '{}'::jsonb,
  outcome_reason text,
  last_error text,
  processed_at timestamptz,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (batch_id, item_key)
);
CREATE INDEX IF NOT EXISTS news_intake_batches_retry_idx
  ON news_intake_batches (status, next_retry_at)
  WHERE status = 'retryable';
CREATE INDEX IF NOT EXISTS news_intake_items_batch_status_idx
  ON news_intake_items (batch_id, status);
-- END migration 0019_news_intake_batch_ledger

-- BEGIN migration 0020_news_articles_review_required_status (0020_news_articles_review_required_status.sql)
-- EP047 — news_articles.status was checked against ('draft','published','archived') only
-- (migration 0013), but news-actions.ts (and the Drizzle schema comment) has used
-- 'review_required' as a valid status since the date-evidence/duplicate-hold feature was
-- added. Any draft needing review (incomplete date evidence, or a duplicate event match)
-- violates the old constraint and fails to save at all — this is the most likely cause of
-- the "review queue shows no articles" report: the insert never actually committed.
ALTER TABLE news_articles DROP CONSTRAINT IF EXISTS news_articles_status_check;
ALTER TABLE news_articles ADD CONSTRAINT news_articles_status_check
  CHECK (status IN ('draft', 'review_required', 'published', 'archived'));
-- END migration 0020_news_articles_review_required_status

-- BEGIN migration 0021_owner_review_intake (0021_owner_review_intake.sql)
-- migrations/0021_owner_review_intake.sql — Durable capability-protected owner review submissions.
--
-- VERSION HISTORY
-- v1.0.0 · 2026-08-05 · Adds hashed owner-review links, immutable decisions, and per-page structured feedback without mail transport.
CREATE TABLE IF NOT EXISTS owner_review_links (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(), business_id uuid NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
  token_hash text NOT NULL UNIQUE, expires_at timestamptz NOT NULL, opened_at timestamptz, submitted_at timestamptz, revoked_at timestamptz,
  created_by_user_id uuid REFERENCES users(id), created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS owner_review_submissions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(), link_id uuid NOT NULL UNIQUE REFERENCES owner_review_links(id),
  business_id uuid NOT NULL REFERENCES businesses(id) ON DELETE CASCADE, decision text NOT NULL CHECK (decision IN ('accept','change','decline')),
  submitted_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS owner_review_page_responses (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(), submission_id uuid NOT NULL REFERENCES owner_review_submissions(id) ON DELETE CASCADE,
  page_key text NOT NULL, no_action_required boolean NOT NULL DEFAULT true, selections jsonb NOT NULL DEFAULT '[]'::jsonb,
  anything_else text NOT NULL DEFAULT '', page_open_date_time timestamptz, UNIQUE(submission_id, page_key)
);
CREATE INDEX IF NOT EXISTS owner_review_links_business_idx ON owner_review_links(business_id, created_at DESC);
CREATE INDEX IF NOT EXISTS owner_review_submissions_business_idx ON owner_review_submissions(business_id, submitted_at DESC);
-- END migration 0021_owner_review_intake

-- BEGIN migration 0022_owner_review_reissue_delivery (0022_owner_review_reissue_delivery.sql)
-- migrations/0022_owner_review_reissue_delivery.sql — Adds the separately audited owner-review invitation type.
--
-- VERSION HISTORY
-- v1.0.0 · 2026-08-05 · Extends the controlled preview-delivery audit enum without changing business state.
--
-- This migration is additive in behavior: it only permits a distinct audit
-- message type for an admin-authorized owner-review invitation. Do not run it
-- without an authorized migration operation.
ALTER TABLE preview_delivery_messages
  DROP CONSTRAINT IF EXISTS preview_delivery_messages_message_type_check;
ALTER TABLE preview_delivery_messages
  ADD CONSTRAINT preview_delivery_messages_message_type_check CHECK (message_type IN (
    'preview_ready', 'owner_review_invitation', 'eta', 'ready_for_activation',
    'reminder_intake', 'reminder_review', 'reminder_activation'
  ));
-- END migration 0022_owner_review_reissue_delivery

-- BEGIN migration 0023_site_in_review_stage (0023_site_in_review_stage.sql)
-- EXCLUDED non-DDL or review-required statement:
-- -- migrations/0023_site_in_review_stage.sql — adds a post-preview pipeline stage so
-- -- sent businesses disappear from the site-previews selection.
-- --
-- -- VERSION HISTORY
-- -- v1.0.0 · 2026-08-07 · Adds site_in_review after ready_for_preview. Once the
-- --   preview-ready email is sent the business moves here and no longer appears
-- --   in the send list (which queries ready_for_preview). A future stage
-- --   (e.g. approved, changes_requested) or activation step follows this.
--
-- INSERT INTO pipeline_stages (key, label, sort_order, board_column, is_terminal, sla_hours)
-- VALUES ('site_in_review', 'Site in Review', 13, 'Website', false, 168)
-- ON CONFLICT (key) DO NOTHING;
-- END migration 0023_site_in_review_stage

-- BEGIN migration 0024_verification_batch_send_status (0024_verification_batch_send_status.sql)
-- EXCLUDED non-DDL or review-required statement:
-- -- Permit durable aggregate outcomes produced by explicit batch email sending.
-- -- Per-recipient delivery remains the source of truth;
-- EXCLUDED non-DDL or review-required statement:
-- this is an audit summary only.
-- ALTER TABLE verification_batches DROP CONSTRAINT IF EXISTS verification_batches_status_check;
ALTER TABLE verification_batches ADD CONSTRAINT verification_batches_status_check
  CHECK (status IN ('prepared','partially_ready','ready','cancelled','sent','partially_sent','failed'));
-- END migration 0024_verification_batch_send_status

-- BEGIN migration 0025_crm_reporting_tables (0025_crm_reporting_tables.sql)
-- migrations/0024_cultured_eddie_brock.sql — EP043 CRM reporting tables.
--
-- VERSION HISTORY
-- v1.0.0 · 2026-08-10 · Adds message_versions, outreach_responses, and
--   commercial_opportunities, plus verification_deliveries.message_version_id.
--   Hand-trimmed from the drizzle-kit auto-generated diff: the raw diff also
--   re-emitted CREATE TABLE for owner_review_links/owner_review_submissions/
--   owner_review_page_responses, which already exist in the live DB (created
--   by migration 0021 via hand-written SQL, never generated through
--   drizzle-kit) — the snapshot lineage under migrations/meta only has
--   0000/0002/0018, so drizzle-kit's diff engine has no record of 0019-0023's
--   hand-written changes and believed those tables were still new. Applying
--   the un-trimmed file would fail on a live DB. See task
--   workstream/200_inprogress/ep047-crm/20260810_042109_ep047_997_crm_lane2_batch_reporting.md.
CREATE TABLE "commercial_opportunities" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"business_id" uuid NOT NULL,
	"stage" text DEFAULT 'listing_claimed' NOT NULL,
	"claimed_at" timestamp with time zone,
	"activation_value" double precision,
	"activated_at" timestamp with time zone,
	"service_type" text,
	"service_value" double precision,
	"converted_at" timestamp with time zone,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	"updated_at" timestamp with time zone DEFAULT now() NOT NULL,
	CONSTRAINT "commercial_opportunities_business_id_unique" UNIQUE("business_id")
);
--> statement-breakpoint
CREATE TABLE "message_versions" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"template_name" text NOT NULL,
	"version_number" integer NOT NULL,
	"subject" text NOT NULL,
	"body" text NOT NULL,
	"campaign_ref" text,
	"date_introduced" timestamp with time zone DEFAULT now() NOT NULL,
	"date_retired" timestamp with time zone,
	"created_by_user_id" uuid,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "outreach_responses" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"business_id" uuid NOT NULL,
	"delivery_id" uuid,
	"batch_item_id" uuid,
	"message_version_id" uuid,
	"channel" text DEFAULT 'email' NOT NULL,
	"original_body" text NOT NULL,
	"classification" text NOT NULL,
	"received_at" timestamp with time zone DEFAULT now() NOT NULL,
	"recorded_by_user_id" uuid,
	"notes" text
);
--> statement-breakpoint
ALTER TABLE "verification_deliveries" ADD COLUMN "message_version_id" uuid;
--> statement-breakpoint
ALTER TABLE "commercial_opportunities" ADD CONSTRAINT "commercial_opportunities_business_id_businesses_id_fk" FOREIGN KEY ("business_id") REFERENCES "public"."businesses"("id") ON DELETE cascade ON UPDATE no action;
--> statement-breakpoint
ALTER TABLE "message_versions" ADD CONSTRAINT "message_versions_created_by_user_id_users_id_fk" FOREIGN KEY ("created_by_user_id") REFERENCES "public"."users"("id") ON DELETE no action ON UPDATE no action;
--> statement-breakpoint
ALTER TABLE "outreach_responses" ADD CONSTRAINT "outreach_responses_business_id_businesses_id_fk" FOREIGN KEY ("business_id") REFERENCES "public"."businesses"("id") ON DELETE cascade ON UPDATE no action;
--> statement-breakpoint
ALTER TABLE "outreach_responses" ADD CONSTRAINT "outreach_responses_delivery_id_verification_deliveries_id_fk" FOREIGN KEY ("delivery_id") REFERENCES "public"."verification_deliveries"("id") ON DELETE no action ON UPDATE no action;
--> statement-breakpoint
ALTER TABLE "outreach_responses" ADD CONSTRAINT "outreach_responses_batch_item_id_verification_batch_items_id_fk" FOREIGN KEY ("batch_item_id") REFERENCES "public"."verification_batch_items"("id") ON DELETE no action ON UPDATE no action;
--> statement-breakpoint
ALTER TABLE "outreach_responses" ADD CONSTRAINT "outreach_responses_message_version_id_message_versions_id_fk" FOREIGN KEY ("message_version_id") REFERENCES "public"."message_versions"("id") ON DELETE no action ON UPDATE no action;
--> statement-breakpoint
ALTER TABLE "outreach_responses" ADD CONSTRAINT "outreach_responses_recorded_by_user_id_users_id_fk" FOREIGN KEY ("recorded_by_user_id") REFERENCES "public"."users"("id") ON DELETE no action ON UPDATE no action;
--> statement-breakpoint
CREATE INDEX "commercial_opportunities_stage_idx" ON "commercial_opportunities" USING btree ("stage");
--> statement-breakpoint
CREATE UNIQUE INDEX "message_versions_template_version_uidx" ON "message_versions" USING btree ("template_name","version_number");
--> statement-breakpoint
CREATE INDEX "message_versions_template_idx" ON "message_versions" USING btree ("template_name");
--> statement-breakpoint
CREATE INDEX "outreach_responses_business_idx" ON "outreach_responses" USING btree ("business_id","received_at");
--> statement-breakpoint
CREATE INDEX "outreach_responses_classification_idx" ON "outreach_responses" USING btree ("classification","received_at");
--> statement-breakpoint
CREATE INDEX "outreach_responses_message_version_idx" ON "outreach_responses" USING btree ("message_version_id");
--> statement-breakpoint
CREATE INDEX "outreach_responses_batch_item_idx" ON "outreach_responses" USING btree ("batch_item_id");
--> statement-breakpoint
ALTER TABLE "verification_deliveries" ADD CONSTRAINT "verification_deliveries_message_version_id_message_versions_id_fk" FOREIGN KEY ("message_version_id") REFERENCES "public"."message_versions"("id") ON DELETE no action ON UPDATE no action;
-- END migration 0025_crm_reporting_tables
