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

test.before(async () => {
  temporary = await mkdtemp(path.join(os.tmpdir(), "assistant-platform-"));
  await writeFile(path.join(temporary, "clients.json"), await readFile(path.join(projectRoot, "data", "clients.json")));
  await writeFile(path.join(temporary, "records.json"), JSON.stringify({ conversations: [], leads: [], callbacks: [], bookings: [] }));
  server = await createApp({ store: new JsonStore(temporary), env: { ADMIN_TOKEN: "test-secret", OPENAI_API_KEY: "", NOTIFICATION_WEBHOOK_URL: "" } });
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
  const admin = await request("/admin");
  assert.equal(admin.status, 200);
  assert.match(admin.body, /Client profiles/);
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

test("assistant answers from approved knowledge and records the conversation", async () => {
  const response = await request("/api/public/chat", { method: "POST", body: { clientKey: "demo_northstar", host: "localhost", sessionId: "test-session", message: "How much is an annual boiler service?" } });
  assert.equal(response.status, 200);
  assert.match(response.body.reply.text, /£95/);
  assert.deepEqual(response.body.reply.sources.map((item) => item.id), ["pricing"]);
  const records = await request("/api/admin/records", { token: "test-secret" });
  assert.equal(records.body.records.conversations.length, 1);
  assert.equal(records.body.records.conversations[0].clientId, "northstar-heating");
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
