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
