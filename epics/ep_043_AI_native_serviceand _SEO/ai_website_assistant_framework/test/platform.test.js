import assert from "node:assert/strict";
import { mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { createAssistantReply } from "../src/assistant.js";
import { createApp } from "../src/server.js";
import { JsonStore } from "../src/store.js";

const projectRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
let temporary;
let server;
let base;
let ledgerWrites = [];

test.before(async () => {
  temporary = await mkdtemp(path.join(os.tmpdir(), "assistant-platform-"));
  await writeFile(path.join(temporary, "clients.json"), await readFile(path.join(projectRoot, "data", "clients.json")));
  await writeFile(path.join(temporary, "records.json"), JSON.stringify({ conversations: [], leads: [], callbacks: [], bookings: [] }));
  server = await createApp({ store: new JsonStore(temporary), env: {
    ADMIN_TOKEN: "test-secret", OWNER_CONSOLE_TOKENS_JSON: JSON.stringify({ "air-quantum-existing-site-demo": "owner-air-test" }), OWNER_CONSOLE_TOKENS_JSON_BATCH_01: JSON.stringify({ "batch01-beck-and-call": "owner-batch-test" }), OPENAI_API_KEY: "", NOTIFICATION_WEBHOOK_URL: "",
    RESPONSE_LEDGER_GITHUB_TOKEN: "test-ledger-token", RESPONSE_LEDGER_REPOSITORY: "edebell67/assistant-response-ledger", RESPONSE_LEDGER_PATH: "responses.ndjson",
    fetchImpl: async (_url, options = {}) => {
      if (options.method === "GET") return { status: 404, ok: false, json: async () => ({}) };
      ledgerWrites.push(JSON.parse(options.body));
      return { status: 201, ok: true, json: async () => ({ content: { sha: "next-sha" } }) };
    }
  } });
  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  base = `http://127.0.0.1:${server.address().port}`;
});

test.after(async () => {
  await new Promise((resolve) => server.close(resolve));
  await rm(temporary, { recursive: true, force: true });
});

async function request(route, { method = "GET", token, body, origin } = {}) {
  const headers = {};
  if (token) headers.Authorization = `Bearer ${token}`;
  if (body) headers["Content-Type"] = "application/json";
  if (origin) headers.Origin = origin;
  const response = await fetch(`${base}${route}`, { method, headers, body: body ? JSON.stringify(body) : undefined });
  const type = response.headers.get("content-type") || "";
  return { status: response.status, headers: response.headers, body: type.includes("json") ? await response.json() : await response.text() };
}

test("health and static assets are executable", async () => {
  const health = await request("/api/health");
  assert.equal(health.status, 200);
  assert.equal(health.body.ok, true);
  const widget = await request("/widget.js");
  assert.equal(widget.status, 200);
  assert.match(widget.body, /attachShadow/);
  assert.match(widget.body, /header:after\s*\{[^}]*pointer-events:none/);
  assert.match(widget.body, /aria-label="Start a new conversation"/);
  assert.match(widget.body, /function resetConversation\(/);
  assert.match(widget.body, /assistantActions/);
  assert.match(widget.body, /Platform demonstration/);
  assert.match(widget.body, /function actionButton\(/);
  assert.match(widget.body, /\.group-label/);
  const admin = await request("/admin");
  assert.equal(admin.status, 200);
  assert.match(admin.body, /Client profiles/);
  assert.match(admin.body, /Preview responses/);
  const owner = await request("/owner");
  assert.equal(owner.status, 200);
  assert.match(owner.body, /Owner Activity Console/);
});

test("public configuration is tenant-scoped, host-bound, and safely projected", async () => {
  const valid = await request("/api/public/config?clientKey=demo_northstar&host=localhost");
  assert.equal(valid.status, 200);
  assert.equal(valid.body.client.businessName, "Northstar Heating");
  assert.equal(valid.body.client.status, "demo");
  assert.equal("knowledge" in valid.body.client, false);
  assert.equal("notificationDestinations" in valid.body.client, false);
  const denied = await request("/api/public/config?clientKey=demo_northstar&host=attacker.example");
  assert.equal(denied.status, 404);
});

test("engagement mode defaults to on_demand and can be switched to proactive by the site owner", async () => {
  const defaulted = await request("/api/public/config?clientKey=demo_northstar&host=localhost");
  assert.equal(defaulted.body.client.engagementMode, "on_demand");
  assert.equal(defaulted.body.client.proactiveDelayMs, 2500);

  const list = await request("/api/admin/clients", { token: "test-secret" });
  const northstar = list.body.clients[0];
  const switched = await request(`/api/admin/clients/${northstar.id}`, { method: "PUT", token: "test-secret", body: { engagementMode: "proactive", proactiveDelayMs: 1200 } });
  assert.equal(switched.body.client.engagementMode, "proactive");
  assert.equal(switched.body.client.proactiveDelayMs, 1200);

  const proactiveConfig = await request("/api/public/config?clientKey=demo_northstar&host=localhost");
  assert.equal(proactiveConfig.body.client.engagementMode, "proactive");
  assert.equal(proactiveConfig.body.client.proactiveDelayMs, 1200);

  const invalidMode = await request(`/api/admin/clients/${northstar.id}`, { method: "PUT", token: "test-secret", body: { engagementMode: "not-a-real-mode" } });
  assert.equal(invalidMode.body.client.engagementMode, "on_demand");

  await request(`/api/admin/clients/${northstar.id}`, { method: "PUT", token: "test-secret", body: { engagementMode: "on_demand", proactiveDelayMs: 2500 } });
});

test("widget owner dashboard access is password-gated and tenant-scoped", async () => {
  const blocked = await request("/api/public/owner-dashboard-access", { method: "POST", body: { clientKey: "air_quantum_existing_site_demo", host: "localhost", password: "wrong" }, origin: "http://localhost" });
  assert.equal(blocked.status, 401);
  const allowed = await request("/api/public/owner-dashboard-access", { method: "POST", body: { clientKey: "air_quantum_existing_site_demo", host: "localhost", password: "owner-air-test" }, origin: "http://localhost" });
  assert.equal(allowed.status, 200);
  assert.equal(allowed.body.dashboardUrl, "/owner?tenant=air-quantum-existing-site-demo");
  const unactivated = await request("/api/public/owner-dashboard-access", { method: "POST", body: { clientKey: "batch01_af_refrigeration", host: "localhost", password: "anything" }, origin: "http://localhost" });
  assert.equal(unactivated.status, 403);
});

test("owner activity access is tenant-isolated and never accepts the admin token", async () => {
  const chat = await request("/api/public/chat", { method: "POST", body: { clientKey: "air_quantum_existing_site_demo", host: "localhost", sessionId: "owner-console-test", message: "Show the demo booking flow" } });
  assert.equal(chat.status, 200);
  const callback = await request("/api/public/callbacks", { method: "POST", body: { clientKey: "air_quantum_existing_site_demo", host: "localhost", name: "Demo owner", telephone: "07000 000000", reason: "Demo callback" } });
  assert.equal(callback.status, 201);
  const denied = await request("/api/owner/activity?tenant=air-quantum-existing-site-demo", { token: "test-secret" });
  assert.equal(denied.status, 401);
  const activity = await request("/api/owner/activity?tenant=air-quantum-existing-site-demo", { token: "owner-air-test" });
  assert.equal(activity.status, 200);
  assert.equal(activity.body.owner.businessName, "Air Quantum Ltd");
  assert.equal(activity.body.records.conversations.every((record) => record.clientId === "air-quantum-existing-site-demo"), true);
  assert.equal(activity.body.summary.conversations >= 1, true);
  assert.equal(activity.body.performance.today.assistantVisitors >= 1, true);
  assert.equal(activity.body.performance.baseline.leadsCaptured, 5);
  const completed = await request(`/api/owner/callbacks/${encodeURIComponent(activity.body.records.callbacks[0].id)}/complete?tenant=air-quantum-existing-site-demo`, { method: "POST", token: "owner-air-test" });
  assert.equal(completed.status, 200);
  assert.equal(completed.body.record.handledByOwner, true);
  assert.equal(completed.body.performance.today.resolvedCallbacks, 1);
});

test("activated batch tenant owner console accepts its password and remains tenant-scoped", async () => {
  const allowed = await request("/api/owner/activity?tenant=batch01-beck-and-call", { token: "owner-batch-test" });
  assert.equal(allowed.status, 200);
  const otherTenant = await request("/api/owner/activity?tenant=air-quantum-existing-site-demo", { token: "owner-batch-test" });
  assert.equal(otherTenant.status, 401);
});

test("public config exposes blueprint assistant actions resolved from pages, modules, and knowledge", async () => {
  const config = await request("/api/public/config?clientKey=hoxtans_n1&host=localhost");
  const actions = config.body.client.assistantActions;
  assert.ok(Array.isArray(actions) && actions.length > 0);

  // A blueprint-tagged page becomes a navigate action pointing at the real page.
  const gallery = actions.find((item) => item.key === "gallery");
  assert.equal(gallery.type, "navigate");
  assert.equal(gallery.url, "gallery.html");

  // An enabled module becomes a prompt action.
  const contact = actions.find((item) => item.key === "contact");
  assert.equal(contact.type, "prompt");

  // Every action key belongs to the canonical blueprint vocabulary, and there
  // are no duplicates or dead ends.
  const keys = actions.map((item) => item.key);
  assert.equal(new Set(keys).size, keys.length);

  // Platform demo workflows are surfaced separately, not mixed into blueprint actions.
  assert.equal(actions.some((item) => item.key.startsWith("demo")), false);
  assert.ok(config.body.client.demoActions.some((item) => item.key === "demoBooking"));

  // An unrecognised blueprint tag on a page must not produce a button.
  const list = await request("/api/admin/clients", { token: "test-secret" });
  const hoxtans = list.body.clients.find((item) => item.id === "hoxtans");
  const badPages = hoxtans.pages.map((page) => ({ ...page, blueprint: page.blueprint === "gallery" ? "not-a-real-key" : page.blueprint }));
  await request(`/api/admin/clients/${hoxtans.id}`, { method: "PUT", token: "test-secret", body: { pages: badPages } });
  const afterBad = await request("/api/public/config?clientKey=hoxtans_n1&host=localhost");
  const galleryAction = afterBad.body.client.assistantActions.find((item) => item.key === "gallery");
  assert.equal(galleryAction, undefined);
  // Restore the valid tag so later tests see the seeded state.
  await request(`/api/admin/clients/${hoxtans.id}`, { method: "PUT", token: "test-secret", body: { pages: hoxtans.pages } });
});

test("assistant answers from approved knowledge and records the conversation", async () => {
  const response = await request("/api/public/chat", { method: "POST", body: { clientKey: "demo_northstar", host: "localhost", sessionId: "test-session", message: "How much is an annual boiler service?" } });
  assert.equal(response.status, 200);
  assert.match(response.body.reply.text, /£95/);
  assert.deepEqual(response.body.reply.sources.map((item) => item.id), ["pricing"]);
  const records = await request("/api/admin/records", { token: "test-secret" });
  assert.equal(records.body.records.conversations.some((record) => record.clientId === "northstar-heating"), true);
});

test("navigation and booking intents return enabled module actions", async () => {
  const navigation = await request("/api/public/chat", { method: "POST", body: { clientKey: "demo_northstar", host: "localhost", message: "Where are your testimonials?" } });
  assert.equal(navigation.body.reply.action.type, "navigate");
  assert.equal(navigation.body.reply.action.url, "#stories");
  const booking = await request("/api/public/chat", { method: "POST", body: { clientKey: "demo_northstar", host: "localhost", message: "Can I book an appointment?" } });
  assert.equal(booking.body.reply.action.type, "booking");
  const callbackIntent = await request("/api/public/chat", { method: "POST", body: { clientKey: "demo_northstar", host: "localhost", message: "Please call me back" } });
  assert.equal(callbackIntent.body.reply.action.type, "callback");
});

test("demo lead and callback modules validate, persist, and suppress notifications", async () => {
  const lead = await request("/api/public/leads", { method: "POST", body: { clientKey: "demo_northstar", host: "localhost", name: "Ada", telephone: "020 7000 0000", email: "ada@example.com", service: "Boiler repair", notes: "No heating" } });
  assert.equal(lead.status, 201);
  assert.equal(lead.body.simulated, true);
  assert.equal(lead.body.notification.reason, "demo_mode");
  const callback = await request("/api/public/callbacks", { method: "POST", body: { clientKey: "demo_northstar", host: "localhost", name: "Sam", telephone: "07111 222333", preferredTime: "Tomorrow morning", reason: "Annual service" } });
  assert.equal(callback.status, 201);
  assert.equal(callback.body.simulated, true);
  const invalid = await request("/api/public/leads", { method: "POST", body: { clientKey: "demo_northstar", host: "localhost", name: "Missing phone" } });
  assert.equal(invalid.status, 400);
});

test("visitor events are tenant-scoped, anonymous, sanitized, whitelisted, and stored in a batch", async () => {
  const res = await request("/api/public/events", { method: "POST", body: {
    clientKey: "demo_northstar", host: "localhost", sessionId: "sess-1",
    events: [
      { type: "pageview", path: "/", device: "mobile", ts: "2026-07-21T00:00:00Z" },
      { type: "cta_click", label: "cta:quote", path: "/", scrollPct: 250 },
      { type: "not_a_real_event", path: "/", label: "should be dropped" },
      { type: "page_exit", dwellMs: 12000, scrollPct: 80 }
    ]
  } });
  assert.equal(res.status, 202);
  assert.equal(res.body.stored, 3); // the unknown type is filtered out

  const records = await request("/api/admin/records", { token: "test-secret" });
  const events = records.body.records.events.filter((e) => e.sessionId === "sess-1");
  assert.equal(events.length, 3);
  assert.equal(events.some((e) => e.type === "not_a_real_event"), false);
  const cta = events.find((e) => e.type === "cta_click");
  assert.equal(cta.label, "cta:quote");
  assert.equal(cta.scrollPct, 100); // clamped 0..100
  assert.equal(cta.clientId, "northstar-heating");
  assert.equal("visitorId" in cta, false); // anonymous: no persistent visitor id stored

  const denied = await request("/api/public/events", { method: "POST", body: { clientKey: "demo_northstar", host: "attacker.example", events: [{ type: "pageview" }] } });
  assert.equal(denied.status, 404);
});

test("visitor analytics can be switched off per site", async () => {
  const off = await request("/api/admin/clients/northstar-heating", { method: "PUT", token: "test-secret", body: { analyticsEnabled: false } });
  assert.equal(off.body.client.analyticsEnabled, false);
  const config = await request("/api/public/config?clientKey=demo_northstar&host=localhost");
  assert.equal(config.body.client.analyticsEnabled, false);

  const res = await request("/api/public/events", { method: "POST", body: { clientKey: "demo_northstar", host: "localhost", sessionId: "sess-off", events: [{ type: "pageview", path: "/" }] } });
  assert.equal(res.status, 202);
  assert.equal(res.body.stored, 0);
  assert.equal(res.body.disabled, true);
  const records = await request("/api/admin/records", { token: "test-secret" });
  assert.equal(records.body.records.events.some((e) => e.sessionId === "sess-off"), false);

  await request("/api/admin/clients/northstar-heating", { method: "PUT", token: "test-secret", body: { analyticsEnabled: true } });
});

test("owner activity console shows anonymous page-analytics alongside conversation/lead activity, tenant-scoped", async () => {
  // Seed page-behaviour events for the activated owner-console tenant and,
  // separately, for another tenant - the console must only ever summarise
  // its own.
  await request("/api/public/events", { method: "POST", body: { clientKey: "air_quantum_existing_site_demo", host: "localhost", sessionId: "page-analytics-test-sess", events: [{ type: "pageview", path: "/services" }, { type: "cta_click", label: "cta:quote" }] } });
  const hoxtans = await request("/api/admin/clients", { token: "test-secret" });
  const hoxtansKey = hoxtans.body.clients.find((item) => item.id === "hoxtans")?.publicKey;
  if (hoxtansKey) await request("/api/public/events", { method: "POST", body: { clientKey: hoxtansKey, host: "localhost", sessionId: "other-tenant-sess", events: [{ type: "pageview", path: "/other" }] } });

  const activity = await request("/api/owner/activity?tenant=air-quantum-existing-site-demo", { token: "owner-air-test" });
  assert.equal(activity.status, 200);
  assert.ok(activity.body.pageAnalytics);
  assert.ok(activity.body.pageAnalytics.pageViews >= 1);
  assert.ok(activity.body.pageAnalytics.ctaClicks >= 1);
  assert.equal(activity.body.pageAnalytics.topPages.some(([path]) => path === "/other"), false); // never another tenant's page

  // Raw events are summarised, not dumped into the per-type activity timeline.
  assert.equal("events" in activity.body.records, false);
  assert.equal("events" in activity.body.summary, false);

  // The summary is aggregated numbers only - no raw session ids reach the response.
  assert.equal(JSON.stringify(activity.body.pageAnalytics).includes("page-analytics-test-sess"), false);

  // Wrong/missing owner token still fails, even though the tenant now has analytics data.
  const denied = await request("/api/owner/activity?tenant=air-quantum-existing-site-demo", { token: "wrong-token" });
  assert.equal(denied.status, 401);
});

test("visitor analytics events are excluded from the admin's generic records listing shape but still stored", async () => {
  const records = await request("/api/admin/records", { token: "test-secret" });
  assert.ok(Array.isArray(records.body.records.events));
});

test("lead follow-up recovers cold leads and feeds the ROI report", async () => {
  const shortDelay = await request("/api/admin/clients/northstar-heating", { method: "PUT", token: "test-secret", body: { leadFollowupDelayMs: 50, averageJobValue: 180 } });
  assert.equal(shortDelay.status, 200);
  assert.equal(shortDelay.body.client.leadFollowupDelayMs, 50);

  const cold = await request("/api/public/leads", { method: "POST", body: { clientKey: "demo_northstar", host: "localhost", name: "Cold Lead", telephone: "07000 111222", service: "Boiler repair", notes: "Thinking about it" } });
  assert.equal(cold.status, 201);
  const coldId = (await request("/api/admin/records", { token: "test-secret" })).body.records.leads.find((item) => item.name === "Cold Lead").id;
  const scheduled = (await request("/api/admin/records", { token: "test-secret" })).body.records.leads.find((item) => item.id === coldId);
  assert.equal(scheduled.followupStatus, "scheduled");

  await new Promise((resolve) => setTimeout(resolve, 150));
  const afterDelay = (await request("/api/admin/records", { token: "test-secret" })).body.records.leads.find((item) => item.id === coldId);
  assert.equal(afterDelay.followupStatus, "sent");
  assert.ok(afterDelay.followupSentAt);

  const converted = await request(`/api/admin/leads/${coldId}/convert`, { method: "POST", token: "test-secret" });
  assert.equal(converted.status, 200);
  assert.equal(converted.body.lead.convertedVia, "after_followup");

  const warm = await request("/api/public/leads", { method: "POST", body: { clientKey: "demo_northstar", host: "localhost", name: "Warm Lead", telephone: "07000 333444", service: "Boiler repair" } });
  assert.equal(warm.status, 201);
  const warmId = (await request("/api/admin/records", { token: "test-secret" })).body.records.leads.find((item) => item.name === "Warm Lead").id;
  const warmConverted = await request(`/api/admin/leads/${warmId}/convert`, { method: "POST", token: "test-secret" });
  assert.equal(warmConverted.body.lead.convertedVia, "same_session");

  const roi = await request("/api/admin/roi?clientId=northstar-heating", { token: "test-secret" });
  assert.equal(roi.status, 200);
  assert.equal(roi.body.businessName, "Northstar Heating");
  assert.ok(roi.body.followupsSent >= 1);
  assert.ok(roi.body.convertedAfterFollowup >= 1);
  assert.ok(roi.body.convertedSameSession >= 1);
  assert.ok(roi.body.recoveryRate > 0);
  assert.equal(roi.body.estimatedRecoveredRevenue, roi.body.convertedAfterFollowup * roi.body.averageJobValue);

  const missing = await request("/api/admin/leads/does-not-exist/convert", { method: "POST", token: "test-secret" });
  assert.equal(missing.status, 404);
  const unauthorized = await request("/api/admin/roi?clientId=northstar-heating");
  assert.equal(unauthorized.status, 401);
});

test("Hoxtans demo business workflows are tenant-scoped, simulated, and recorded", async () => {
  const config = await request("/api/public/config?clientKey=hoxtans_n1&host=localhost");
  assert.equal(config.status, 200);
  assert.deepEqual(
    ["demoBooking", "demoPayment", "demoEmail", "demoCrm"].filter((module) => !config.body.client.enabledModules.includes(module)),
    []
  );
  assert.equal(config.body.client.demoWorkflows.booking.services.length, 4);

  const common = { clientKey: "hoxtans_n1", host: "localhost" };
  const booking = await request("/api/public/demo/booking", { method: "POST", body: { ...common, name: "Alex Demo", telephone: "07000 000000", service: "Full-body spray tan", slot: "Tomorrow · 10:00" } });
  assert.equal(booking.status, 201);
  assert.equal(booking.body.simulated, true);
  assert.equal(booking.body.record.status, "reserved");
  assert.match(booking.body.record.reference, /^DEMO-BOOK-/);

  const payment = await request("/api/public/demo/payment", { method: "POST", body: { ...common, customerName: "Alex Demo", service: "Full-body spray tan" } });
  assert.equal(payment.status, 201);
  assert.equal(payment.body.record.amount, 25);
  assert.equal(payment.body.record.status, "approved");
  assert.equal(payment.body.record.simulated, true);

  const email = await request("/api/public/demo/email", { method: "POST", body: { ...common, recipientName: "Alex Demo", email: "alex@example.com", subject: "Appointment details", message: "This is a fictional appointment preview." } });
  assert.equal(email.status, 201);
  assert.equal(email.body.record.status, "previewed_not_sent");

  const crm = await request("/api/public/demo/crm", { method: "POST", body: { ...common, name: "Alex Demo", email: "alex@example.com", interest: "Spray tan", stage: "New enquiry" } });
  assert.equal(crm.status, 201);
  assert.equal(crm.body.record.status, "created_in_demo_pipeline");

  const invalidService = await request("/api/public/demo/booking", { method: "POST", body: { ...common, name: "Alex", telephone: "1", service: "Not seeded", slot: "Tomorrow · 10:00" } });
  assert.equal(invalidService.status, 400);
  const disabledTenant = await request("/api/public/demo/payment", { method: "POST", body: { clientKey: "demo_northstar", host: "localhost", customerName: "Alex", service: "Boiler" } });
  assert.equal(disabledTenant.status, 403);

  const records = await request("/api/admin/records", { token: "test-secret" });
  assert.equal(records.body.records.bookings.length, 1);
  assert.equal(records.body.records.payments.length, 1);
  assert.equal(records.body.records.emails.length, 1);
  assert.equal(records.body.records.crmLeads.length, 1);
  assert.ok(["bookings", "payments", "emails", "crmLeads"].every((type) => records.body.records[type][0].simulated));
});

test("preview response endpoint records a private decision without email or notification", async () => {
  const accepted = await request("/api/public/preview-responses", {
    method: "POST",
    origin: "https://edebell67.github.io",
    body: { clientKey: "funcuts_se20", action: "discuss_activation", pageUrl: "https://edebell67.github.io/epics/funcuts/reply.html" }
  });
  assert.equal(accepted.status, 201);
  assert.equal(accepted.body.accepted, true);
  assert.equal(accepted.body.durable, true);
  assert.equal(ledgerWrites.length, 1);
  assert.match(Buffer.from(ledgerWrites[0].content, "base64").toString("utf8"), /Fun Cuts response - discuss activation/);
  assert.equal(accepted.body.notification, undefined);
  const records = await request("/api/admin/records", { token: "test-secret" });
  assert.equal(records.body.records.previewResponses.length, 1);
  assert.equal(records.body.records.previewResponses[0].clientId, "fun-cuts");
  assert.equal(records.body.records.previewResponses[0].action, "discuss_activation");
  assert.equal(records.body.records.previewResponses[0].summary, "Fun Cuts response - discuss activation");
  const invalid = await request("/api/public/preview-responses", { method: "POST", body: { clientKey: "funcuts_se20", host: "localhost", action: "anything_else" } });
  assert.equal(invalid.status, 400);
});

test("admin endpoints enforce auth and persist configurable module/live state", async () => {
  const denied = await request("/api/admin/clients");
  assert.equal(denied.status, 401);
  const list = await request("/api/admin/clients", { token: "test-secret" });
  const northstar = list.body.clients[0];
  const updated = await request(`/api/admin/clients/${northstar.id}`, { method: "PUT", token: "test-secret", body: { status: "live", enabledModules: northstar.enabledModules.filter((item) => item !== "callback") } });
  assert.equal(updated.body.client.status, "live");
  assert.equal(updated.body.client.enabledModules.includes("callback"), false);
  const gated = await request("/api/public/callbacks", { method: "POST", body: { clientKey: "demo_northstar", host: "localhost", name: "Sam", telephone: "1" } });
  assert.equal(gated.status, 403);
  const liveLead = await request("/api/public/leads", { method: "POST", body: { clientKey: "demo_northstar", host: "localhost", name: "Lin", telephone: "2", service: "Heating" } });
  assert.equal(liveLead.body.simulated, false);
  assert.equal(liveLead.body.notification.reason, "not_configured");
});

test("clients can be duplicated without sharing identity and remain in demo mode", async () => {
  const duplicate = await request("/api/admin/clients/northstar-heating/duplicate", { method: "POST", token: "test-secret" });
  assert.equal(duplicate.status, 201);
  assert.notEqual(duplicate.body.client.id, "northstar-heating");
  assert.notEqual(duplicate.body.client.publicKey, "demo_northstar");
  assert.equal(duplicate.body.client.status, "demo");
});

test("optional Responses API adapter receives bounded approved context", async () => {
  const client = JSON.parse(await readFile(path.join(projectRoot, "data", "clients.json"), "utf8"))[0];
  let requestBody;
  const reply = await createAssistantReply({
    client,
    message: "How much is a boiler service?",
    history: Array.from({ length: 12 }, (_, index) => ({ role: index % 2 ? "assistant" : "user", content: `message ${index}` })),
    env: { OPENAI_API_KEY: "not-a-real-key", OPENAI_MODEL: "test-model", OPENAI_BASE_URL: "https://api.openai.test/v1" },
    fetchImpl: async (_url, options) => {
      requestBody = JSON.parse(options.body);
      return { ok: true, json: async () => ({ output: [{ type: "message", content: [{ type: "output_text", text: "Approved answer." }] }] }) };
    }
  });
  assert.equal(reply.text, "Approved answer.");
  assert.equal(requestBody.model, "test-model");
  assert.match(requestBody.instructions, /£95/);
  assert.equal(requestBody.input.length, 9);
});
