/**
 * epics/ep_047_newssite_app/tests/import-news-batches.test.js — regression coverage for private News intake dry-run safety.
 *
 * VERSION HISTORY
 * v1.0.0 · 2026-08-03 · Initial version: proves dry run creates a private report without contacting the receiver.
 */
import assert from "node:assert/strict";
import { mkdtemp, readFile, rm } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { spawn } from "node:child_process";
import { batchHash } from "../src/intake.js";

const appRoot = path.resolve(import.meta.dirname, "..");

function runDryRun(reportPath) {
  return new Promise((resolve, reject) => {
    const child = spawn(process.execPath, ["scripts/import-news-batches.js", "--dry-run", "--report", reportPath], {
      cwd: appRoot,
      env: {
        ...process.env,
        NEWS_IMPORT_API_URL: "http://127.0.0.1:1/receiver-must-not-be-contacted",
        NEWS_IMPORT_API_KEY: "test-key-must-not-be-used",
      },
      stdio: ["ignore", "pipe", "pipe"],
    });
    let stdout = "";
    let stderr = "";
    child.stdout.on("data", (data) => { stdout += data; });
    child.stderr.on("data", (data) => { stderr += data; });
    child.on("error", reject);
    child.on("close", (code) => resolve({ code, stdout, stderr }));
  });
}

test("batch hash is canonical regardless of JSON key order", () => {
  assert.equal(batchHash({ b: 2, a: { z: 1, y: 3 } }), batchHash({ a: { y: 3, z: 1 }, b: 2 }));
});

test("dry run validates private batches and never attempts delivery", async () => {
  const tempDir = await mkdtemp(path.join(os.tmpdir(), "ep047-news-dry-run-"));
  const reportPath = path.join(tempDir, "report.json");
  try {
    const result = await runDryRun(reportPath);
    assert.equal(result.code, 0, result.stderr);
    assert.match(result.stdout, /no receiver request, database write, deployment, or public-content action was attempted/);
    const report = JSON.parse(await readFile(reportPath, "utf8"));
    assert.equal(report.mode, "dry-run");
    assert.equal(report.deliveryAttempted, false);
    assert.equal(report.publicContentCreated, false);
    assert.equal(report.databaseWriteAttempted, false);
    assert.equal(report.batches.length, 2);
    assert.deepEqual(report.batches.map((batch) => batch.itemCount), [3, 3]);
  } finally {
    await rm(tempDir, { recursive: true, force: true });
  }
});
