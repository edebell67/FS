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
--> statement-breakpoint
INSERT INTO validation_policy(id, allow_partial_verification) VALUES (1, false)
  ON CONFLICT (id) DO NOTHING;
--> statement-breakpoint
INSERT INTO validation_field_rules(field_name, label, rule_type, mandatory, blocks_verification)
VALUES
  ('businessName', 'Business name', 'presence', true, true),
  ('category', 'Category', 'presence', true, true),
  ('email', 'Email', 'email', false, false),
  ('phone', 'Phone', 'phone', false, false),
  ('website', 'Website', 'url', false, false)
ON CONFLICT DO NOTHING;
--> statement-breakpoint
ALTER TABLE verification_links
  ADD COLUMN IF NOT EXISTS validation_status_at_issue text,
  ADD COLUMN IF NOT EXISTS validation_run_id uuid REFERENCES business_validation_runs(id),
  ADD COLUMN IF NOT EXISTS outstanding_fields jsonb NOT NULL DEFAULT '[]'::jsonb;
