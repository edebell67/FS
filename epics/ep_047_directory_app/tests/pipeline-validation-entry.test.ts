import assert from "node:assert/strict";
import test from "node:test";
import { readFile } from "node:fs/promises";

test("pipeline exposes validation state separately from historic Imported stage", async () => {
  const page = await readFile(new URL("../app/directoryadmin/pipeline/page.tsx", import.meta.url), "utf8");
  assert.match(page, /getValidationOverview/);
  assert.match(page, /ValidationOverviewPanel/);
  assert.match(page, /href="\/directoryadmin\/validation"/);
  assert.match(page, /Run field validation for/);
  assert.match(page, /awaitingValidation/);
  assert.match(page, /Open field validation/);
  assert.match(page, /Select validated businesses for batch verification/);
});

test("completed validation synchronises the durable pipeline projection", async () => {
  const validationRepository = await readFile(
    new URL("../lib/validation/repository.ts", import.meta.url), "utf8",
  );
  const importRepository = await readFile(
    new URL("../lib/import/repository.ts", import.meta.url), "utf8",
  );
  const synchroniser = await readFile(
    new URL("../lib/validation/pipeline-sync.ts", import.meta.url), "utf8",
  );

  assert.match(validationRepository, /result\.status === "validated"/);
  assert.match(validationRepository, /synchroniseValidatedPipelineStage\(tx, businessId, now\)/);
  assert.match(importRepository, /result\.status === "validated"/);
  assert.match(importRepository, /synchroniseValidatedPipelineStage\(tx, inserted\.id, now\)/);
  assert.match(synchroniser, /current_stage\.sort_order < target_stage\.sort_order/);
  assert.match(synchroniser, /FOR UPDATE OF business/);
  assert.match(synchroniser, /source = 'automation'/);
  assert.match(synchroniser, /field_validation_completed/);
  assert.match(synchroniser, /ON CONFLICT DO NOTHING/);
});

test("backfill moves only fully validated Imported businesses using validation timestamps", async () => {
  const migration = await readFile(
    new URL("../migrations/0007_validation_pipeline_sync.sql", import.meta.url), "utf8",
  );

  assert.match(migration, /business\.validation_status = 'validated'/);
  assert.match(migration, /business\.current_stage_id = imported\.id/);
  assert.match(migration, /COALESCE\(\s*business\.validated_at,\s*validation_run\.completed_at/s);
  assert.match(migration, /stage_transitions_validation_completed_uidx/);
  assert.match(migration, /WHERE source = 'automation' AND reason = 'field_validation_completed'/);
  assert.match(migration, /WHERE NOT EXISTS/);
  assert.match(migration, /ON CONFLICT DO NOTHING/);
  assert.doesNotMatch(migration, /partially_validated|non_valid/);
});
