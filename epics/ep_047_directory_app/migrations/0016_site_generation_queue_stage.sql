-- EP047: introduces an explicit queue stage between Claimed and site
-- generation being usable, and renames the post-generation stage to match
-- the agreed terminology (ready_for_preview). Additive/rename only -- no
-- stage is removed, no business row's history is altered beyond the stage
-- label/key rename, which is purely presentational.

-- Make room at sort_order 11 for the new stage.
UPDATE pipeline_stages SET sort_order = sort_order + 1 WHERE sort_order >= 11;

INSERT INTO pipeline_stages (key, label, sort_order, board_column, is_terminal, sla_hours) VALUES
  ('awaiting_site_generation', 'Awaiting Site Generation', 11, 'Website', false, 24)
ON CONFLICT (key) DO NOTHING;

-- The stage previously called "Website Generated" is the same event as what
-- the agreed design now calls "ready_for_preview": generation is complete
-- and the business is ready for the preview-ready notification.
UPDATE pipeline_stages
SET key = 'ready_for_preview', label = 'Ready for Preview'
WHERE key = 'website_generated';
