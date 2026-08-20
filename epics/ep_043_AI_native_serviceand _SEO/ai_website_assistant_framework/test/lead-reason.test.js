import assert from "node:assert/strict";
import { mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { createApp } from "../src/server.js";
import { JsonStore, normalizeClient } from "../src/store.js";

const frameworkRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

test("serviceReasonMap: entries pointing outside leadReasonOptions are dropped at normalize time", () => {
  const normalized = normalizeClient({
    id: "map-test", businessName: "Map Test", enabledModules: ["leadCapture"],
    leadReasonOptions: ["ai automation", "other"],
    serviceReasonMap: { "AI site assistants": "ai automation", "Some Other Service": "not-a-real-option" }
  });
  assert.deepEqual(normalized.serviceReasonMap, { "AI site assistants": "ai automation" }, "the invalid mapping is silently dropped, not stored as garbage data");
});

test("reasonForVisit: exposed to the widget, validated on submit, and segmented for the owner", async (t) => {
  const temporary = await mkdtemp(path.join(os.tmpdir(), "lead-reason-"));
  await writeFile(path.join(temporary, "clients.json"), await readFile(path.join(frameworkRoot, "data", "clients.json")));
  await writeFile(path.join(temporary, "records.json"), JSON.stringify({
    conversations: [], leads: [], callbacks: [], bookings: [], payments: [], emails: [], crmLeads: [], events: [], questionFollowups: []
  }));
  const server = await createApp({
    store: new JsonStore(temporary),
    env: { ADMIN_TOKEN: "test-admin", OPENAI_API_KEY: "", NODE_ENV: "production", ASSISTANT_ENQUIRY_DELIVERY_MODE: "directory-gmail", ASSISTANT_ENQUIRY_DELIVERY_APPROVED: "true", DIRECTORY_ENQUIRY_DELIVERY_URL: "https://directory.internal/api/internal/assistant-enquiries", DIRECTORY_ENQUIRY_DELIVERY_KEY: "test-internal-key", fetchImpl: async () => Response.json({ accepted: true, providerMessageId: "test-provider-id" }, { status: 201 }), BUSINESS_OWNER_TOKENS_JSON: JSON.stringify({ "the-tech-principle-local": "test-owner" }) }
  });
  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  const base = `http://127.0.0.1:${server.address().port}`;
  const request = async (route, { method = "GET", body, token } = {}) => {
    const response = await fetch(`${base}${route}`, {
      method, headers: { ...(body ? { "Content-Type": "application/json" } : {}), ...(token ? { Authorization: `Bearer ${token}` } : {}) },
      body: body ? JSON.stringify(body) : undefined
    });
    return { status: response.status, body: await response.json() };
  };
  t.after(async () => { await new Promise((resolve) => server.close(resolve)); await rm(temporary, { recursive: true, force: true }); });

  // 1. The widget reads the six options from public config.
  const config = await request("/api/public/config?clientKey=thetechprinciple_local&host=thetechprinciple.com");
  assert.equal(config.status, 200);
  assert.deepEqual(config.body.client.leadReasonOptions, ["website audit", "website build", "ai automation", "application build", "mobile apps", "other"]);
  assert.equal(config.body.client.serviceReasonMap["AI site assistants"], "ai automation", "the widget's pre-select map is exposed alongside the options");
  assert.equal(config.body.client.serviceReasonMap["Web design & rebuilds"], "website build");

  // A client with leadCapture disabled must not leak its options even if configured.
  const otherConfig = await request("/api/public/config?clientKey=demo_northstar&host=localhost");
  assert.equal(otherConfig.status, 200);
  assert.deepEqual(otherConfig.body.client.leadReasonOptions, [], "clients without leadReasonOptions configured are unaffected");

  // 2. An invalid value is rejected.
  const invalid = await request("/api/public/leads", { method: "POST", body: {
    clientKey: "thetechprinciple_local", host: "thetechprinciple.com", name: "Sam", telephone: "07000000000", reasonForVisit: "not-a-real-option"
  } });
  assert.equal(invalid.status, 400);

  // 2b. A missing value is rejected too — the widget's required <select> is
  // not a substitute for server-side enforcement (a direct API call or a
  // bypassed form must not be able to skip it).
  const missing = await request("/api/public/leads", { method: "POST", body: {
    clientKey: "thetechprinciple_local", host: "thetechprinciple.com", name: "NoReason", telephone: "07000000002"
  } });
  assert.equal(missing.status, 400);
  assert.match(missing.body.error, /required/i);

  // 3. A valid value is accepted and stored.
  const valid = await request("/api/public/leads", { method: "POST", body: {
    clientKey: "thetechprinciple_local", host: "thetechprinciple.com", name: "Priya", telephone: "07123456789", reasonForVisit: "ai automation"
  } });
  assert.equal(valid.status, 201);

  const second = await request("/api/public/leads", { method: "POST", body: {
    clientKey: "thetechprinciple_local", host: "thetechprinciple.com", name: "Jordan", telephone: "07123456780", reasonForVisit: "ai automation"
  } });
  assert.equal(second.status, 201);

  const third = await request("/api/public/leads", { method: "POST", body: {
    clientKey: "thetechprinciple_local", host: "thetechprinciple.com", name: "Alex", telephone: "07123456781", reasonForVisit: "mobile apps"
  } });
  assert.equal(third.status, 201);

  // A client without leadReasonOptions is not required to send one at all.
  const noReason = await request("/api/public/leads", { method: "POST", body: {
    clientKey: "demo_northstar", host: "localhost", name: "No Reason", telephone: "07000000001"
  } });
  assert.equal(noReason.status, 201, "clients without configured options don't require reasonForVisit");

  // 4. The owner sees the segmented breakdown.
  const reporting = await request("/api/owner/reporting?tenant=the-tech-principle-local", { token: "test-owner" });
  assert.equal(reporting.status, 200);
  assert.deepEqual(reporting.body.leadsByReason, { "ai automation": 2, "mobile apps": 1 });
});
