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
