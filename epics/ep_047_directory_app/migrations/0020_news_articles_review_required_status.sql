-- EP047 — news_articles.status was checked against ('draft','published','archived') only
-- (migration 0013), but news-actions.ts (and the Drizzle schema comment) has used
-- 'review_required' as a valid status since the date-evidence/duplicate-hold feature was
-- added. Any draft needing review (incomplete date evidence, or a duplicate event match)
-- violates the old constraint and fails to save at all — this is the most likely cause of
-- the "review queue shows no articles" report: the insert never actually committed.
ALTER TABLE news_articles DROP CONSTRAINT IF EXISTS news_articles_status_check;
ALTER TABLE news_articles ADD CONSTRAINT news_articles_status_check
  CHECK (status IN ('draft', 'review_required', 'published', 'archived'));
