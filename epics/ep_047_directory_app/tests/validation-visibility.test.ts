import assert from "node:assert/strict";
import test from "node:test";
import { readFile } from "node:fs/promises";
import {
  formatValidationDuration,
  formatValidationStatus,
  formatValidationTimestamp,
} from "../lib/validation/presentation";

test("validation run presentation includes explicit timezone, duration and readable status", () => {
  const timestamp = formatValidationTimestamp(new Date("2026-01-01T12:34:56Z"));
  assert.match(timestamp, /GMT/);
  assert.match(timestamp, /\(Europe\/London\)$/);
  assert.equal(formatValidationDuration({
    startedAt: new Date("2026-01-01T12:00:00Z"),
    completedAt: new Date("2026-01-01T13:02:03Z"),
  }), "1h 2m");
  assert.equal(formatValidationStatus("completed_with_errors"), "completed with errors");
});

test("dashboard and pipeline show all outcome counts and latest run details", async () => {
  const [dashboard, pipeline, panel] = await Promise.all([
    readFile(new URL("../app/directoryadmin/dashboard/page.tsx", import.meta.url), "utf8"),
    readFile(new URL("../app/directoryadmin/pipeline/page.tsx", import.meta.url), "utf8"),
    readFile(new URL("../components/admin/ValidationOverviewPanel.tsx", import.meta.url), "utf8"),
  ]);
  assert.match(dashboard, /ValidationOverviewPanel/);
  assert.match(pipeline, /ValidationOverviewPanel/);
  for (const label of ["Validated", "Partially validated", "Non-valid", "Awaiting validation"]) {
    assert.match(panel, new RegExp(label));
  }
  for (const label of ["Status", "Processed", "Errors", "Duration", "Started", "Completed"]) {
    assert.match(panel, new RegExp(`>${label}<`));
  }
});

test("validation counts distinguish awaiting records and imported SLA ignores completed validation", async () => {
  const [validationRepository, pipelineQueries] = await Promise.all([
    readFile(new URL("../lib/validation/repository.ts", import.meta.url), "utf8"),
    readFile(new URL("../lib/db/queries/pipeline.ts", import.meta.url), "utf8"),
  ]);
  assert.match(validationRepository, /lastValidationRunId} IS NULL/);
  assert.match(validationRepository, /validationStatus} = 'partially_validated'/);
  assert.match(validationRepository, /validationStatus} = 'non_valid'/);
  assert.match(validationRepository, /validationStatus} = 'validated'/);
  assert.match(pipelineQueries, /key} <> 'imported' OR \$\{businesses\.lastValidationRunId} IS NULL/g);
});
