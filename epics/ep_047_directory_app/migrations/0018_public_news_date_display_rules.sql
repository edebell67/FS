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
INSERT INTO public_news_display_settings (id) VALUES (true) ON CONFLICT (id) DO NOTHING;

CREATE INDEX IF NOT EXISTS news_articles_effective_public_idx
  ON news_articles (status, town, effective_story_date DESC, published_at DESC);
CREATE INDEX IF NOT EXISTS news_articles_event_identity_idx
  ON news_articles (event_identity) WHERE event_identity IS NOT NULL;
