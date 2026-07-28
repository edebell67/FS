-- EP047: Public launch scope and database-backed hyperlocal news.
-- These tables are deliberately additive. Visibility controls public output;
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
