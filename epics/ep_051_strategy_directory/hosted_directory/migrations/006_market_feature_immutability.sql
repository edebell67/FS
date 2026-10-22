-- EP051 hosted market evidence immutability and deterministic point-in-time identity.
BEGIN;

DO $$
BEGIN
  IF EXISTS (
    SELECT 1 FROM intelligence_market_feature
    GROUP BY market,as_of HAVING count(*)>1
  ) THEN
    RAISE EXCEPTION 'Cannot enforce market feature immutability: duplicate market/as_of rows require operator reconciliation';
  END IF;
END $$;

ALTER TABLE intelligence_market_feature DROP CONSTRAINT IF EXISTS intelligence_market_feature_pkey;
ALTER TABLE intelligence_market_feature ADD PRIMARY KEY(market,as_of);

COMMIT;
