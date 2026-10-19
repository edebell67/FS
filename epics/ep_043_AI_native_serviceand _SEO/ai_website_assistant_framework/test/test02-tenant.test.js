import assert from "node:assert/strict";
import { mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { createApp } from "../src/server.js";
import { JsonStore } from "../src/store.js";

const frameworkRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

test("Test02 private preview resolves only on its approved host and keeps external capture disabled", async (t) => {
  const dataDir = await mkdtemp(path.join(os.tmpdir(), "test02-tenant-"));
  await writeFile(path.join(dataDir, "clients.json"), await readFile(path.join(frameworkRoot, "data", "clients.json")));
  await writeFile(path.join(dataDir, "records.json"), JSON.stringify({ conversations: [], leads: [], callbacks: [], bookings: [], payments: [], emails: [], crmLeads: [], events: [], questionFollowups: [] }));
  const server = await createApp({ store: new JsonStore(dataDir), env: { ADMIN_TOKEN: "test-admin", OPENAI_API_KEY: "", NOTIFICATION_WEBHOOK_URL: "" } });
  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  t.after(async () => { await new Promise((resolve) => server.close(resolve)); await rm(dataDir, { recursive: true, force: true }); });
  const base = `http://127.0.0.1:${server.address().port}`;
  const fetchConfig = async (host) => { const r = await fetch(`${base}/api/public/config?clientKey=test02_prospect_ltd&host=${host}`); return { status: r.status, body: await r.json() }; };

  const approved = await fetchConfig("thetechprinciple.com");
  assert.equal(approved.status, 200);
  assert.equal(approved.body.client.status, "demo");
  assert.deepEqual(approved.body.client.enabledModules.sort(), ["assistant", "contact", "faq", "navigation"]);
  assert.equal(approved.body.client.enabledModules.includes("leadCapture"), false);
  assert.match(approved.body.client.tagline, /private/i);

  const rejected = await fetchConfig("attacker.example");
  assert.equal(rejected.status, 404);
});
