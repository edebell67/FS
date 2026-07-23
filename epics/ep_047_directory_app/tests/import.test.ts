import { test } from "node:test";
import assert from "node:assert/strict";

import { importFile } from "../lib/import/import-file";
import { InMemoryImportRepository } from "../lib/import/in-memory-repository";
import { parseCsv } from "../lib/import/csv";
import { parseJson } from "../lib/import/json";
import { deriveCategoryCode, generateBusinessRef, createInMemorySequenceProvider } from "../lib/import/business-ref";
import { isValidEmail, isValidPhone, isValidWebsite } from "../lib/import/validators";

test("parseCsv extracts columns and rows from a header row", () => {
  const csv = `Business Name,Category,Town,Email\nAcme Plumbing,Plumbing,Bristol,info@acme.co.uk\n`;
  const parsed = parseCsv(csv);
  assert.deepEqual(parsed.columns, ["Business Name", "Category", "Town", "Email"]);
  assert.equal(parsed.rows.length, 1);
  assert.equal(parsed.rows[0]!["Business Name"], "Acme Plumbing");
});

test("parseJson accepts a flat array of records", () => {
  const parsed = parseJson(JSON.stringify([{ "Business Name": "Acme", Category: "Plumbing" }]));
  assert.equal(parsed.rows.length, 1);
  assert.ok(parsed.columns.includes("Business Name"));
});

test("parseJson rejects a non-array payload", () => {
  assert.throws(() => parseJson(JSON.stringify({ not: "an array" })));
});

test("validators reject obvious garbage without being over-strict", () => {
  assert.equal(isValidEmail("info@acme.co.uk"), true);
  assert.equal(isValidEmail("not-an-email"), false);
  assert.equal(isValidWebsite("acme.co.uk"), true);
  assert.equal(isValidWebsite("https://acme.co.uk/services"), true);
  assert.equal(isValidWebsite("not a url"), false);
  assert.equal(isValidPhone("+44 117 496 0000"), true);
  assert.equal(isValidPhone("abc"), false);
});

test("deriveCategoryCode and generateBusinessRef produce the TP-XXXXX-000001 shape", async () => {
  assert.equal(deriveCategoryCode("Plumbing"), "PLUMB");
  const provider = createInMemorySequenceProvider();
  const first = await generateBusinessRef("Plumbing", provider);
  const second = await generateBusinessRef("Plumbing", provider);
  assert.equal(first, "TP-PLUMB-000001");
  assert.equal(second, "TP-PLUMB-000002");
});

test("importFile accepts a clean CSV row end to end", async () => {
  const csv = `Business Name,Category,Town,Email,Phone\nAcme Plumbing,Plumbing,Bristol,info@acme.co.uk,+44 117 496 0000\n`;
  const repository = new InMemoryImportRepository();

  const { batchId, summary } = await importFile({
    filename: "test.csv",
    content: csv,
    source: "csv",
    repository,
  });

  assert.equal(summary.accepted.length, 1);
  assert.equal(summary.rejected.length, 0);
  assert.equal(summary.accepted[0]!.businessRef, "TP-PLUMB-000001");
  assert.equal(repository.businessesByBatch.get(batchId)?.length, 1);
  assert.equal(repository.batchStatus.get(batchId), "completed");
});

test("importFile rejects rows missing required fields and reports the row number", async () => {
  const csv = `Business Name,Category\n,Plumbing\nAcme Electrics,\n`;
  const repository = new InMemoryImportRepository();

  const { summary } = await importFile({
    filename: "test.csv",
    content: csv,
    source: "csv",
    repository,
  });

  assert.equal(summary.accepted.length, 0);
  assert.equal(summary.rejected.length, 2);
  assert.equal(summary.rejected[0]!.rowNumber, 1);
  assert.equal(summary.rejected[0]!.code, "missing_required_field");
});

test("importFile drops an invalid email but still imports the business (email is optional)", async () => {
  const csv = `Business Name,Category,Email\nAcme Plumbing,Plumbing,not-an-email\n`;
  const repository = new InMemoryImportRepository();

  const { summary } = await importFile({
    filename: "test.csv",
    content: csv,
    source: "csv",
    repository,
  });

  assert.equal(summary.accepted.length, 1);
  assert.equal(summary.rejected.length, 0);
  assert.equal(summary.warnings.length, 1);
  assert.equal(summary.warnings[0]!.code, "invalid_email");
  assert.equal(summary.warnings[0]!.kind, "warning");
  assert.equal(summary.accepted[0]!.input.email, undefined);
});

test("importFile still rejects a row missing a required field even if it also has a bad optional field", async () => {
  const csv = `Business Name,Category,Email\n,Plumbing,not-an-email\n`;
  const repository = new InMemoryImportRepository();

  const { summary } = await importFile({
    filename: "test.csv",
    content: csv,
    source: "csv",
    repository,
  });

  assert.equal(summary.accepted.length, 0);
  assert.equal(summary.rejected.length, 1);
  assert.equal(summary.rejected[0]!.code, "missing_required_field");
  // the bad email on a row that never gets imported shouldn't also show up as a warning
  assert.equal(summary.warnings.length, 0);
});

test("importFile imports a business with a multi-number phone field as a warning, not a rejection", async () => {
  // Real data found in UK_Ltd_email_no_website_VERIFIED_410.csv: some rows list
  // two phone numbers comma-separated in one field. That's not a reason to
  // lose the whole business.
  const csv = `Business Name,Category,Phone\nAcme Plumbing,Plumbing,"01213733439, 01213733196"\n`;
  const repository = new InMemoryImportRepository();

  const { summary } = await importFile({
    filename: "test.csv",
    content: csv,
    source: "csv",
    repository,
  });

  assert.equal(summary.accepted.length, 1);
  assert.equal(summary.rejected.length, 0);
  assert.equal(summary.warnings.length, 1);
  assert.equal(summary.warnings[0]!.code, "invalid_phone");
  assert.equal(summary.accepted[0]!.input.phone, undefined);
});

test("importFile flags a duplicate within the same batch", async () => {
  const csv = [
    "Business Name,Category,Email",
    "Acme Plumbing,Plumbing,info@acme.co.uk",
    "Acme Plumbing Ltd,Plumbing,info@acme.co.uk",
  ].join("\n");
  const repository = new InMemoryImportRepository();

  const { summary } = await importFile({
    filename: "test.csv",
    content: csv,
    source: "csv",
    repository,
  });

  assert.equal(summary.accepted.length, 1);
  assert.equal(summary.duplicates.length, 1);
  assert.equal(summary.duplicates[0]!.code, "duplicate_in_batch");
  assert.equal(summary.duplicates[0]!.rowNumber, 2);
});

test("importFile flags a duplicate against an existing record", async () => {
  const csv = `Business Name,Category,Email\nAcme Plumbing,Plumbing,info@acme.co.uk\n`;
  const repository = new InMemoryImportRepository([
    { email: "info@acme.co.uk", namePart: "", postcodePart: "" },
  ]);

  const { summary } = await importFile({
    filename: "test.csv",
    content: csv,
    source: "csv",
    repository,
  });

  assert.equal(summary.accepted.length, 0);
  assert.equal(summary.duplicates.length, 1);
  assert.equal(summary.duplicates[0]!.code, "duplicate_existing");
});

test("importFile flags a duplicate against an existing record with no email/phone/website (name+postcode only)", async () => {
  // Regression test: found via UK_Ltd_email_no_website_VERIFIED_410.csv, where
  // most rows have none of email/phone/website. DrizzleImportRepository's
  // existingLookup originally only checked those three fields and returned
  // false immediately when none were present on the row — meaning a business
  // like this could never be caught as a duplicate against the DB, only
  // within the same file. "Appliance Repair Express Ltd" got imported twice
  // as a result before this was fixed.
  const csv = `Business Name,Category,Town\nAppliance Repair Express Ltd,Appliance Repairs,Birmingham\n`;
  const repository = new InMemoryImportRepository([
    { namePart: "appliancerepairexpressltd", postcodePart: "" },
  ]);

  const { summary } = await importFile({
    filename: "test.csv",
    content: csv,
    source: "csv",
    repository,
  });

  assert.equal(summary.accepted.length, 0);
  assert.equal(summary.duplicates.length, 1);
  assert.equal(summary.duplicates[0]!.code, "duplicate_existing");
});

test("importFile handles JSON input identically to CSV", async () => {
  const json = JSON.stringify([{ "Business Name": "Acme Plumbing", Category: "Plumbing" }]);
  const repository = new InMemoryImportRepository();

  const { summary } = await importFile({
    filename: "test.json",
    content: json,
    source: "json",
    repository,
  });

  assert.equal(summary.accepted.length, 1);
  assert.equal(summary.accepted[0]!.businessRef, "TP-PLUMB-000001");
});

test("rollbackBatch removes every business the batch created", async () => {
  const csv = [
    "Business Name,Category",
    "Acme Plumbing,Plumbing",
    "Beta Electrics,Electrical",
  ].join("\n");
  const repository = new InMemoryImportRepository();

  const { batchId } = await importFile({
    filename: "test.csv",
    content: csv,
    source: "csv",
    repository,
  });

  assert.equal(repository.businessesByBatch.get(batchId)?.length, 2);
  const deletedCount = await repository.rollbackBatch(batchId);
  assert.equal(deletedCount, 2);
  assert.equal(repository.businessesByBatch.get(batchId)?.length, 0);
  assert.equal(repository.batchStatus.get(batchId), "rolled_back");
});
