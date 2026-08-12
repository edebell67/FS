import assert from "node:assert/strict";
import { mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { createApp } from "../src/server.js";
import { JsonStore } from "../src/store.js";

const frameworkRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

test("GET /api/public/highlights: filters by service, no auth required, and highlight_impression/click events are ingestible", async (t) => {
  const temporary = await mkdtemp(path.join(os.tmpdir(), "highlights-"));
  await writeFile(path.join(temporary, "clients.json"), await readFile(path.join(frameworkRoot, "data", "clients.json")));
  await writeFile(path.join(temporary, "records.json"), JSON.stringify({
    conversations: [], leads: [], callbacks: [], bookings: [], payments: [], emails: [], crmLeads: [], events: [], questionFollowups: []
  }));
  const server = await createApp({ store: new JsonStore(temporary), env: { ADMIN_TOKEN: "test-admin", OPENAI_API_KEY: "", NOTIFICATION_WEBHOOK_URL: "" } });
  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  const base = `http://127.0.0.1:${server.address().port}`;
  const request = async (route, opts = {}) => {
    const response = await fetch(`${base}${route}`, opts);
    return { status: response.status, body: await response.json(), headers: response.headers };
  };
  t.after(async () => { await new Promise((resolve) => server.close(resolve)); await rm(temporary, { recursive: true, force: true }); });

  const all = await request("/api/public/highlights?tenant=the-tech-principle-local");
  assert.equal(all.status, 200);
  assert.equal(all.body.highlights.length, 6, "all seeded case studies for this client");

  const filtered = await request("/api/public/highlights?tenant=the-tech-principle-local&service=" + encodeURIComponent("AI site assistants"));
  assert.equal(filtered.status, 200);
  assert.equal(filtered.body.highlights.length, 1);
  assert.equal(filtered.body.highlights[0].title, "Website assistant framework");

  const missingTenant = await request("/api/public/highlights");
  assert.equal(missingTenant.status, 400);

  const promotions = await request("/api/public/promotions?tenant=the-tech-principle-local", {
    headers: { Origin: "https://thetechprinciple.com" },
  });
  assert.equal(promotions.status, 200);
  assert.equal(promotions.body.promotions.length, 0);
  assert.equal(promotions.headers.get("access-control-allow-origin"), "https://thetechprinciple.com");

  const events = await request("/api/public/events", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      clientKey: "thetechprinciple_local", host: "thetechprinciple.com", sessionId: "hl-session",
      events: [
        { type: "highlight_impression", path: "/", highlightId: filtered.body.highlights[0].id, service: "AI site assistants" },
        { type: "highlight_click", path: "/", highlightId: filtered.body.highlights[0].id, service: "AI site assistants" }
      ]
    })
  });
  assert.equal(events.status, 202);
  assert.equal(events.body.stored, 2, "both highlight event types pass the ALLOWED_EVENT_TYPES allowlist");

  const admin = await request("/api/admin/records", { headers: { Authorization: "Bearer test-admin" } });
  const stored = admin.body.records.events.filter((item) => item.clientId === "the-tech-principle-local");
  assert.equal(stored.length, 2);
  assert.equal(stored.find((item) => item.type === "highlight_impression").highlightId, filtered.body.highlights[0].id);
});
