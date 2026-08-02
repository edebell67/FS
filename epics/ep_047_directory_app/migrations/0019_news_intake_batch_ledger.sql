-- EP047-2026.08.02.1 — Durable private News JSON intake ledger.
-- Additive only. Imported content is always held as draft or review_required;
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
