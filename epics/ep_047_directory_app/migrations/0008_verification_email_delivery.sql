ALTER TABLE verification_deliveries
  ADD COLUMN IF NOT EXISTS status text NOT NULL DEFAULT 'prepared',
  ADD COLUMN IF NOT EXISTS delivery_mode text NOT NULL DEFAULT 'disabled',
  ADD COLUMN IF NOT EXISTS tracking_key_hash text,
  ADD COLUMN IF NOT EXISTS handoff_started_at timestamptz,
  ADD COLUMN IF NOT EXISTS opened_at timestamptz,
  ADD COLUMN IF NOT EXISTS clicked_at timestamptz,
  ADD COLUMN IF NOT EXISTS completed_at timestamptz,
  ADD COLUMN IF NOT EXISTS revoked_at timestamptz;
--> statement-breakpoint
UPDATE verification_deliveries
SET tracking_key_hash =
  md5(id::text || clock_timestamp()::text) ||
  md5(clock_timestamp()::text || id::text)
WHERE tracking_key_hash IS NULL;
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
