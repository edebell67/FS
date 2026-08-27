-- EP051 idempotent reference seed. Version 1.0.0 (2026-08-23).
-- Strategy descriptive names are intentionally not invented; they are supplied later.
BEGIN;
CREATE TABLE IF NOT EXISTS ep051.reference_data_version (
    reference_key text PRIMARY KEY,
    reference_value text NOT NULL
);
INSERT INTO ep051.reference_data_version(reference_key, reference_value)
VALUES ('seed_version', '1.0.0')
ON CONFLICT (reference_key) DO UPDATE SET reference_value = EXCLUDED.reference_value;
COMMIT;
