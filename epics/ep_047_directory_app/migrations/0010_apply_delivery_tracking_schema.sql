-- High-water-mark forward repair. Earlier delivery-tracking migration entries
-- were recorded before their schema was present in production; this entry is
-- deliberately newer than every existing journal timestamp so Drizzle applies
-- it to that database.
ALTER TABLE verification_deliveries
  ADD COLUMN IF NOT EXISTS tracking_key_hash text,
  ADD COLUMN IF NOT EXISTS handoff_started_at timestamptz,
  ADD COLUMN IF NOT EXISTS opened_at timestamptz,
  ADD COLUMN IF NOT EXISTS clicked_at timestamptz,
  ADD COLUMN IF NOT EXISTS completed_at timestamptz,
  ADD COLUMN IF NOT EXISTS revoked_at timestamptz;
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
