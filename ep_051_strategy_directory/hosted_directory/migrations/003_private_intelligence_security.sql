-- Version history: 1.0.0 (2026-08-24) Enforce mandatory RLS and parent/child tenant ownership on upgraded databases.
BEGIN;

ALTER TABLE intelligence_user_consent FORCE ROW LEVEL SECURITY;
ALTER TABLE intelligence_watchlist FORCE ROW LEVEL SECURITY;
ALTER TABLE intelligence_saved_search FORCE ROW LEVEL SECURITY;
ALTER TABLE intelligence_collection FORCE ROW LEVEL SECURITY;
ALTER TABLE intelligence_collection_strategy FORCE ROW LEVEL SECURITY;
ALTER TABLE intelligence_preference FORCE ROW LEVEL SECURITY;
ALTER TABLE intelligence_user_history FORCE ROW LEVEL SECURITY;
ALTER TABLE intelligence_privacy_audit FORCE ROW LEVEL SECURITY;

DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname='intelligence_collection_collection_owner_key') THEN
    ALTER TABLE intelligence_collection ADD CONSTRAINT intelligence_collection_collection_owner_key UNIQUE(collection_id,owner_id);
  END IF;
  IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname='intelligence_collection_strategy_collection_id_fkey') THEN
    ALTER TABLE intelligence_collection_strategy DROP CONSTRAINT intelligence_collection_strategy_collection_id_fkey;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname='intelligence_collection_strategy_collection_owner_fkey') THEN
    ALTER TABLE intelligence_collection_strategy ADD CONSTRAINT intelligence_collection_strategy_collection_owner_fkey
      FOREIGN KEY(collection_id,owner_id) REFERENCES intelligence_collection(collection_id,owner_id) ON DELETE CASCADE;
  END IF;
END $$;

COMMIT;
