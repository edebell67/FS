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
