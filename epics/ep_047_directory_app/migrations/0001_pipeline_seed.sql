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
-- Cancelled/Archived are terminal and parked in the Subscriber column as
-- exit states rather than getting a ninth column.
INSERT INTO pipeline_stages (key, label, sort_order, board_column, is_terminal, sla_hours) VALUES
  ('discovered',                 'Discovered',                  1,  'Discovered',   false, 72),
  ('imported',                   'Imported',                    2,  'Imported',     false, 24),
  ('validated',                  'Validated',                   3,  'Validated',    false, 24),
  ('categorised',                'Categorised',                 4,  'Validated',    false, 24),
  ('directory_published',        'Directory Published',         5,  'Validated',    false, NULL),
  ('verification_email_pending', 'Verification Email Pending',  6,  'Verification', false, 24),
  ('verification_sent',          'Verification Sent',           7,  'Verification', false, 72),
  ('verification_opened',        'Verification Opened',         8,  'Verification', false, 168),
  ('verification_completed',     'Verification Completed',      9,  'Verification', false, NULL),
  ('business_claimed',           'Business Claimed',            10, 'Claimed',      false, NULL),
  ('website_generated',          'Website Generated',           11, 'Website',      false, 24),
  ('website_viewed',             'Website Viewed',              12, 'Website',      false, 168),
  ('website_ready',              'Website Ready',               13, 'Website',      false, NULL),
  ('publish_requested',          'Publish Requested',           14, 'Website',      false, 48),
  ('website_published',          'Website Published',           15, 'Published',    false, NULL),
  ('ai_assistant_available',     'AI Assistant Available',      16, 'Published',    false, NULL),
  ('ai_assistant_activated',     'AI Assistant Activated',      17, 'Published',    false, NULL),
  ('lead_received',              'Lead Received',                18, 'Published',    false, 24),
  ('customer_contacted',         'Customer Contacted',          19, 'Published',    false, 48),
  ('subscriber',                 'Subscriber',                  20, 'Subscriber',   true,  NULL),
  ('cancelled',                  'Cancelled',                   21, 'Subscriber',   true,  NULL),
  ('archived',                   'Archived',                    22, 'Subscriber',   true,  NULL)
ON CONFLICT (key) DO NOTHING;
