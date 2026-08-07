-- migrations/0023_site_in_review_stage.sql — adds a post-preview pipeline stage so
-- sent businesses disappear from the site-previews selection.
--
-- VERSION HISTORY
-- v1.0.0 · 2026-08-07 · Adds site_in_review after ready_for_preview. Once the
--   preview-ready email is sent the business moves here and no longer appears
--   in the send list (which queries ready_for_preview). A future stage
--   (e.g. approved, changes_requested) or activation step follows this.

INSERT INTO pipeline_stages (key, label, sort_order, board_column, is_terminal, sla_hours)
VALUES ('site_in_review', 'Site in Review', 13, 'Website', false, 168)
ON CONFLICT (key) DO NOTHING;