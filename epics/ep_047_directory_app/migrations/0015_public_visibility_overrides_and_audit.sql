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
