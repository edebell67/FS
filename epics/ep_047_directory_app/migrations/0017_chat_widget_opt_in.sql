-- migrations/0017_chat_widget_opt_in.sql — adds the per-business opt-in flag
-- for the shared AI chat widget that every ep044_group generated site wires
-- in by default.
--
-- VERSION HISTORY
-- v1.0.0 · 2026-07-30 · Initial version: additive boolean column, defaults to
--   true to match the skill's own default (assistant-embed.js ships on by
--   default with a single ASSISTANT_ENABLED flag) — this column is what the
--   generation loop reads to decide that flag's value per business, not a
--   new decision the owner has to make before generation can run.

ALTER TABLE businesses ADD COLUMN IF NOT EXISTS chat_widget_opt_in boolean NOT NULL DEFAULT true;
