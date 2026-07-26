import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { validateBusiness } from "../lib/validation/engine";
import type { ValidationRule } from "../lib/validation/types";

const rules: ValidationRule[] = [
  { id: "name", fieldName: "businessName", label: "Business name", ruleType: "presence", mandatory: true, blocksVerification: true },
  { id: "email", fieldName: "email", label: "Email", ruleType: "email", mandatory: false, blocksVerification: false },
  { id: "phone", fieldName: "phone", label: "Phone", ruleType: "phone", mandatory: false, blocksVerification: false },
  { id: "rating", fieldName: "googleRating", label: "Rating", ruleType: "number_range", mandatory: false, blocksVerification: false, parameters: { min: 0, max: 5 } },
];

test("blank mandatory data deterministically classifies non-valid", () => {
  const first = validateBusiness({ businessName: " " }, rules);
  const second = validateBusiness({ businessName: " " }, [...rules].reverse());
  assert.equal(first.status, "non_valid");
  assert.deepEqual(first, second);
  assert.deepEqual(first.outstandingFields, ["businessName"]);
});

test("malformed optional phone is partial and targeted to phone", () => {
  const result = validateBusiness({ businessName: "Example Ltd", phone: "abc" }, rules);
  assert.equal(result.status, "partially_validated");
  assert.deepEqual(result.outstandingFields, ["phone"]);
  assert.equal(result.outcomes.find((item) => item.fieldName === "phone")?.sourceValue, "abc");
});

test("configured formats and ranges produce validated only when all pass", () => {
  assert.equal(validateBusiness({
    businessName: "Example Ltd", phone: "+44 20 7123 4567",
    email: "owner@example.test", googleRating: 4.5,
  }, rules).status, "validated");
  assert.equal(validateBusiness({
    businessName: "Example Ltd", email: "wrong", googleRating: 9,
  }, rules).status, "partially_validated");
});

test("explicit verification-blocking optional rule classifies failure non-valid", () => {
  const blocking = rules.map((rule) => rule.fieldName === "email" ? { ...rule, blocksVerification: true } : rule);
  assert.equal(validateBusiness({ businessName: "Example", email: "wrong" }, blocking).status, "non_valid");
});

test("migration persists rules, runs, outcomes, repair evidence and policy", async () => {
  const sql = await readFile(new URL("../migrations/0005_field_validation.sql", import.meta.url), "utf8");
  for (const table of ["validation_field_rules", "business_validation_runs", "field_validation_outcomes", "field_repair_history", "validation_policy"]) {
    assert.match(sql, new RegExp(`CREATE TABLE IF NOT EXISTS ${table}`, "i"));
  }
  assert.match(sql, /source_value text/i);
  assert.match(sql, /proposed_value text NOT NULL/i);
  assert.match(sql, /evidence text NOT NULL/i);
  assert.match(sql, /revalidation_run_id uuid/i);
});

test("bulk validation uses a durable, resumable, single-active job ledger", async () => {
  const sql = await readFile(new URL("../migrations/0006_validation_jobs.sql", import.meta.url), "utf8");
  const repository = await readFile(new URL("../lib/validation/repository.ts", import.meta.url), "utf8");
  for (const table of ["validation_jobs", "validation_job_items"]) {
    assert.match(sql, new RegExp(`CREATE TABLE IF NOT EXISTS ${table}`, "i"));
  }
  assert.match(sql, /WHERE status IN \('pending','running'\)/i);
  assert.match(sql, /UNIQUE \(job_id, business_id\)/i);
  assert.match(sql, /validation_job_item_id uuid UNIQUE/i);
  assert.match(repository, /validationJobItemId/);
  assert.match(repository, /VALIDATION_JOB_CHUNK_SIZE = 25/);
  assert.match(repository, /LIMIT \$\{VALIDATION_JOB_CHUNK_SIZE\}/);
  assert.match(repository, /lease_token/);
  assert.match(repository, /status = 'pending', claim_token = NULL/);
  assert.doesNotMatch(repository, /for \(const row of rows\) await runBusinessValidation/);
});

test("admin validation and repair surfaces are session and role protected", async () => {
  const page = await readFile(new URL("../app/directoryadmin/validation/page.tsx", import.meta.url), "utf8");
  const actions = await readFile(new URL("../app/directoryadmin/validation/actions.ts", import.meta.url), "utf8");
  const panel = await readFile(new URL("../app/directoryadmin/validation/ValidationJobPanel.tsx", import.meta.url), "utf8");
  assert.match(page, /requireAdminUserForPage/);
  assert.match(page, /canManageValidation/);
  assert.match(actions, /canManageValidation\(user\.role\)/);
  assert.match(actions, /startBusinessValidationJob/);
  assert.match(actions, /processBusinessValidationJobChunk/);
  assert.match(actions, /applyFieldRepair/);
  assert.match(panel, /processed/);
  assert.match(panel, /Continue \/ resume/);
  assert.match(panel, /errorCount/);
});

test("owner projection exposes flagged field names without internal validation evidence", async () => {
  const repository = await readFile(new URL("../lib/verification/repository.ts", import.meta.url), "utf8");
  const lookup = repository.slice(repository.indexOf("export async function getVerificationByRawToken"), repository.indexOf("export async function submitVerification"));
  assert.match(lookup, /outstandingFields/);
  assert.doesNotMatch(lookup, /fieldValidationOutcomes|fieldRepairHistory|evidence|rulesSnapshot/);
});
