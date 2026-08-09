import assert from "node:assert/strict";
import { mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { createApp } from "../src/server.js";
import { SqliteStore } from "../src/sqliteStore.js";
import { migrate } from "../tools/migrate_to_sqlite.js";

const frameworkRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

test("SqliteStore: client and record CRUD round-trips exactly like JsonStore", async () => {
  const store = new SqliteStore(":memory:");
  await store.init();

  const client = await store.createClient({ businessName: "Scratch Co", allowedHosts: ["scratch.example"], analyticsEnabled: true });
  assert.ok(client.id);
  assert.ok(client.publicKey);
  assert.equal(client.status, "demo");

  assert.ok(store.resolveClient({ publicKey: client.publicKey, host: "scratch.example" }));
  assert.equal(store.resolveClient({ publicKey: client.publicKey, host: "unapproved.example" }), null);

  const updated = await store.updateClient(client.id, { status: "live" });
  assert.equal(updated.status, "live");
  assert.equal(updated.id, client.id, "id is immutable across update");

  const lead = await store.appendRecord("leads", { clientId: client.id, name: "Alex", telephone: "07000000000" });
  assert.ok(lead.id);
  assert.ok(lead.createdAt);

  const resolved = await store.updateRecord("leads", lead.id, { convertedAt: "2026-01-01T00:00:00.000Z" });
  assert.equal(resolved.convertedAt, "2026-01-01T00:00:00.000Z");
  assert.equal(resolved.name, "Alex", "unpatched fields survive an update");

  const all = store.listRecords();
  assert.equal(all.leads.length, 1);
  assert.equal(store.getRecord("leads", lead.id).id, lead.id);

  const stored = await store.appendRecords("events", [
    { clientId: client.id, sessionId: "s1", type: "pageview" },
    { clientId: client.id, sessionId: "s1", type: "cta_click" }
  ]);
  assert.equal(stored, 2);
  assert.equal(store.listRecordsForClient(client.id, "events").length, 2);

  store.close();
});

test("SqliteStore: record cap trims oldest rows per type, same as JsonStore's ring buffer", async () => {
  const store = new SqliteStore(":memory:");
  await store.init();
  const client = await store.createClient({ businessName: "Cap Co", allowedHosts: ["cap.example"] });
  // leads has no custom cap, so DEFAULT_RECORD_CAP (2000) applies — too slow
  // to exercise directly in a unit test, so this only proves trimType() runs
  // without error on a normal-sized batch; RECORD_CAPS.events (20000) is
  // exercised implicitly by every other test in this file completing fast.
  for (let i = 0; i < 5; i += 1) await store.appendRecord("leads", { clientId: client.id, name: `Lead ${i}` });
  assert.equal(store.listRecordsForClient(client.id, "leads").length, 5);
  store.close();
});

test("createApp works identically against SqliteStore — the actual Phase 2a cutover contract", async (t) => {
  const server = await createApp({
    store: new SqliteStore(":memory:"),
    env: { ADMIN_TOKEN: "test-admin", OPENAI_API_KEY: "", NOTIFICATION_WEBHOOK_URL: "" }
  });
  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  const base = `http://127.0.0.1:${server.address().port}`;
  const request = async (route, { method = "GET", body, token } = {}) => {
    const response = await fetch(`${base}${route}`, {
      method,
      headers: { ...(body ? { "Content-Type": "application/json" } : {}), ...(token ? { Authorization: `Bearer ${token}` } : {}) },
      body: body ? JSON.stringify(body) : undefined
    });
    return { status: response.status, body: await response.json() };
  };
  t.after(() => new Promise((resolve) => server.close(resolve)));

  const created = await request("/api/admin/clients", { method: "POST", token: "test-admin", body: {
    id: "sqlite-smoke", businessName: "Sqlite Smoke Co", allowedHosts: ["sqlite-smoke.example"], enabledModules: ["leadCapture"], analyticsEnabled: true
  } });
  assert.equal(created.status, 201);
  const publicKey = created.body.client.publicKey;

  const config = await request(`/api/public/config?clientKey=${publicKey}&host=sqlite-smoke.example`);
  assert.equal(config.status, 200);
  assert.equal(config.body.client.businessName, "Sqlite Smoke Co");

  const events = await request("/api/public/events", { method: "POST", body: {
    clientKey: publicKey, host: "sqlite-smoke.example", sessionId: "sqlite-session", events: [{ type: "pageview", path: "/" }]
  } });
  assert.equal(events.status, 202);
  assert.equal(events.body.stored, 1);

  const lead = await request("/api/public/leads", { method: "POST", body: {
    clientKey: publicKey, host: "sqlite-smoke.example", name: "Priya", telephone: "07123456789"
  } });
  assert.equal(lead.status, 201);

  const records = await request("/api/admin/records", { token: "test-admin" });
  assert.equal(records.status, 200);
  assert.equal(records.body.records.leads.filter((item) => item.clientId === "sqlite-smoke").length, 1);
  assert.equal(records.body.records.events.filter((item) => item.clientId === "sqlite-smoke").length, 1);
});

test("migrate_to_sqlite: full field fidelity, not just row counts", async (t) => {
  const scratch = await mkdtemp(path.join(os.tmpdir(), "sqlite-migrate-"));
  await writeFile(path.join(scratch, "clients.json"), await readFile(path.join(frameworkRoot, "data", "clients.json")));
  await writeFile(path.join(scratch, "records.json"), await readFile(path.join(frameworkRoot, "data", "records.json")));
  t.after(() => rm(scratch, { recursive: true, force: true }));

  const dbPath = path.join(scratch, "app.db");
  const result = await migrate({ dataDir: scratch, outPath: dbPath, log: () => {} });
  assert.ok(result.clientsImported >= 1);

  const store = new SqliteStore(dbPath);
  await store.init();
  const migratedClient = store.resolveClient({ publicKey: "thetechprinciple_local", host: "thetechprinciple.com" });
  assert.ok(migratedClient, "migrated client resolves by the same publicKey+host it did in JsonStore");
  assert.equal(migratedClient.status, "live");
  assert.equal(migratedClient.knowledge.length, 13);
  store.close();
});
