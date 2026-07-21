import { createHash, randomUUID, timingSafeEqual } from "node:crypto";
import { createServer } from "node:http";
import { readFileSync } from "node:fs";
import { readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createAssistantReply } from "./assistant.js";
import { JsonStore } from "./store.js";

const rootDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const publicDir = path.join(rootDir, "public");
const runtimeEnv = loadEnvironment(path.join(rootDir, ".env"));
const dataDir = runtimeEnv.DATA_DIR ? path.resolve(runtimeEnv.DATA_DIR) : path.join(rootDir, "data");
const MIME = { ".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".css": "text/css; charset=utf-8", ".svg": "image/svg+xml", ".json": "application/json; charset=utf-8" };

function json(res, status, body, extraHeaders = {}) {
  res.writeHead(status, { "Content-Type": MIME[".json"], "Cache-Control": "no-store", ...extraHeaders });
  res.end(JSON.stringify(body));
}

function safeEqual(a, b) {
  const left = createHash("sha256").update(String(a)).digest();
  const right = createHash("sha256").update(String(b)).digest();
  return timingSafeEqual(left, right);
}

function adminAuthorized(req, env) {
  const token = req.headers.authorization?.replace(/^Bearer\s+/i, "") || "";
  return Boolean(env.ADMIN_TOKEN && safeEqual(token, env.ADMIN_TOKEN));
}

function ownerConsoleActivated(client) {
  return client.ownerConsole?.activated !== false;
}

function ownerTokenFor(env, clientId) {
  try {
    const maps = ["OWNER_CONSOLE_TOKENS_JSON", "OWNER_CONSOLE_TOKENS_JSON_BATCH_01"].map((key) => JSON.parse(String(env[key] || "{}")));
    return maps.find((tokens) => tokens && typeof tokens === "object" && typeof tokens[clientId] === "string" && tokens[clientId])?.[clientId] || "";
  } catch { return ""; }
}

function ownerPasswordAuthorized(password, env, clientId) {
  const expected = ownerTokenFor(env, clientId);
  return Boolean(expected && safeEqual(password, expected));
}

function ownerAuthorized(req, env, clientId) {
  const token = req.headers.authorization?.replace(/^Bearer\s+/i, "") || "";
  return ownerPasswordAuthorized(token, env, clientId);
}

async function bodyJson(req, maxBytes = 64 * 1024) {
  let raw = "";
  for await (const chunk of req) {
    raw += chunk;
    if (Buffer.byteLength(raw) > maxBytes) throw Object.assign(new Error("Request body is too large."), { status: 413 });
  }
  try { return JSON.parse(raw || "{}"); } catch { throw Object.assign(new Error("Request body must be valid JSON."), { status: 400 }); }
}

function cleanText(value, max, required = false) {
  const cleaned = String(value || "").replace(/[\u0000-\u001f]/g, " ").trim().slice(0, max);
  if (required && !cleaned) throw Object.assign(new Error("A required field is missing."), { status: 400 });
  return cleaned;
}

function requestHost(req, suppliedHost) {
  try { return req.headers.origin ? new URL(req.headers.origin).hostname : suppliedHost || ""; } catch { return suppliedHost || ""; }
}

function corsHeaders(req) {
  return req.headers.origin ? { "Access-Control-Allow-Origin": req.headers.origin, "Vary": "Origin" } : {};
}

function demoReference(prefix) {
  return `DEMO-${prefix}-${randomUUID().slice(0, 8).toUpperCase()}`;
}

function validEmail(value) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

// Whitelist of visitor-analytics event types. Anything else is dropped, so a
// page cannot log arbitrary/PII event names into the store.
const ALLOWED_EVENT_TYPES = new Set([
  "pageview", "page_exit", "scroll_depth", "cta_click", "phone_click",
  "email_click", "whatsapp_click", "form_start", "form_submit",
  "gallery_open", "gallery_view", "assistant_open", "assistant_handoff", "outbound_click"
]);

// Reduce an incoming event to a safe, PII-free, identity-free record. Only a
// bounded set of low-cardinality fields are kept; the session id is ephemeral
// (tab-scoped) with no persistent visitor id, so events cannot be tied to a
// person across visits. Free-text is length-capped and control characters
// stripped by cleanText.
function sanitizeEvent(event, { clientId, sessionId }) {
  const num = (value, max) => {
    const n = Number(value);
    return Number.isFinite(n) ? Math.max(0, Math.min(max, Math.round(n))) : undefined;
  };
  return {
    clientId,
    sessionId,
    type: cleanText(event.type, 40),
    path: cleanText(event.path, 300),          // page path only, never query string with PII
    label: cleanText(event.label, 120),        // e.g. CTA id "cta:quote"
    referrerHost: cleanText(event.referrerHost, 120),
    device: cleanText(event.device, 20),       // "mobile" | "tablet" | "desktop"
    scrollPct: num(event.scrollPct, 100),
    dwellMs: num(event.dwellMs, 86400000),
    ts: cleanText(event.ts, 40)                // client timestamp (ISO)
  };
}

// Aggregate a client's page-behaviour events (from analytics-embed.js) into a
// summary shape for the owner console - counts and rates only, never raw
// per-visitor rows, matching the same anonymity contract as ingestion.
function pageAnalyticsSummary(events) {
  const sessions = new Set(events.map((e) => e.sessionId).filter(Boolean));
  const pageviews = events.filter((e) => e.type === "pageview").length;
  const engagedTypes = new Set(["cta_click", "phone_click", "email_click", "whatsapp_click", "form_start", "form_submit", "assistant_open", "gallery_open"]);
  const engagedSessions = new Set(events.filter((e) => engagedTypes.has(e.type) || (e.type === "scroll_depth" && Number(e.scrollPct) >= 50)).map((e) => e.sessionId));
  const count = (t) => events.filter((e) => e.type === t).length;
  const exits = events.filter((e) => e.type === "page_exit");
  const avg = (arr, key) => arr.length ? Math.round(arr.reduce((sum, e) => sum + (Number(e[key]) || 0), 0) / arr.length) : 0;
  const topN = (key, type) => {
    const counts = {};
    for (const e of events) {
      if (type && e.type !== type) continue;
      const k = e[key] || "—";
      counts[k] = (counts[k] || 0) + 1;
    }
    return Object.entries(counts).sort((a, b) => b[1] - a[1]).slice(0, 10);
  };
  const sess = sessions.size;
  return {
    uniqueVisits: sess,
    pageViews: pageviews,
    engagedVisits: engagedSessions.size,
    engagedPct: sess ? Math.round((engagedSessions.size / sess) * 100) : 0,
    ctaClicks: count("cta_click"),
    phoneTaps: count("phone_click"),
    emailTaps: count("email_click"),
    assistantOpens: count("assistant_open"),
    assistantHandoffs: count("assistant_handoff"),
    avgDwellSeconds: Math.round(avg(exits, "dwellMs") / 1000),
    avgScrollPct: avg(exits, "scrollPct"),
    topPages: topN("path", "pageview"),
    eventBreakdown: topN("type")
  };
}

function ownerPerformance(records, client, now = new Date()) {
  const day = now.toISOString().slice(0, 10);
  const today = Object.fromEntries(Object.entries(records).map(([type, entries]) => [type, entries.filter((entry) => String(entry.createdAt || "").slice(0, 10) === day)]));
  const sessions = new Set((today.conversations || []).map((entry) => entry.sessionId).filter(Boolean));
  const callbacks = today.callbacks || [];
  const handled = callbacks.filter((entry) => entry.handledAt && Date.parse(entry.handledAt) >= Date.parse(entry.createdAt));
  const callbackMinutes = handled.map((entry) => Math.round((Date.parse(entry.handledAt) - Date.parse(entry.createdAt)) / 60000));
  const averageCallbackMinutes = callbackMinutes.length ? Math.round(callbackMinutes.reduce((sum, value) => sum + value, 0) / callbackMinutes.length) : null;
  const visitorCount = sessions.size;
  const leadCount = (today.leads || []).length;
  return {
    today: { date: day, assistantVisitors: visitorCount, leadsCaptured: leadCount, leadRate: visitorCount ? Math.round((leadCount / visitorCount) * 100) : null, callbacks: callbacks.length, averageCallbackMinutes, resolvedCallbacks: handled.length },
    baseline: client.ownerReporting?.baseline || { assistantVisitors: null, leadsCaptured: null, callbacks: null, averageCallbackMinutes: null, source: "No previous baseline supplied." }
  };
}

async function writeResponseLedger({ env, record }) {
  const token = String(env.RESPONSE_LEDGER_GITHUB_TOKEN || "").trim();
  const repository = String(env.RESPONSE_LEDGER_REPOSITORY || "").trim();
  const filePath = String(env.RESPONSE_LEDGER_PATH || "responses.ndjson").trim().replace(/^\/+/, "");
  if (!token || !repository || !filePath) throw Object.assign(new Error("Durable response storage is not configured."), { status: 503 });
  const api = `https://api.github.com/repos/${repository}/contents/${filePath.split("/").map(encodeURIComponent).join("/")}`;
  const headers = { Authorization: `Bearer ${token}`, Accept: "application/vnd.github+json", "User-Agent": "ai-website-assistant" };
  const request = env.fetchImpl || fetch;
  const existing = await request(api, { method: "GET", headers });
  let prior = ""; let sha;
  if (existing.ok) {
    const body = await existing.json();
    prior = Buffer.from(String(body.content || "").replace(/\s/g, ""), "base64").toString("utf8");
    sha = body.sha;
  } else if (existing.status !== 404) {
    throw Object.assign(new Error("The private response ledger could not be read."), { status: 502 });
  }
  const line = `${JSON.stringify({ id: record.id, createdAt: record.createdAt, business: record.businessName, action: record.action, summary: record.summary, pageUrl: record.pageUrl })}\n`;
  const saved = await request(api, { method: "PUT", headers: { ...headers, "Content-Type": "application/json" }, body: JSON.stringify({ message: `Record ${record.summary}`, content: Buffer.from(`${prior}${line}`, "utf8").toString("base64"), ...(sha ? { sha } : {}) }) });
  if (!saved.ok) throw Object.assign(new Error("The private response ledger could not be updated."), { status: 502 });
  return { repository, filePath };
}

async function notify({ env, client, kind, record }) {
  if (client.status !== "live" || !env.NOTIFICATION_WEBHOOK_URL) return { delivered: false, reason: client.status === "demo" ? "demo_mode" : "not_configured" };
  const response = await fetch(env.NOTIFICATION_WEBHOOK_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ kind, clientId: client.id, destinations: client.notificationDestinations, record })
  });
  return { delivered: response.ok, reason: response.ok ? "sent" : `webhook_${response.status}` };
}

// Recovers a lead that didn't convert in-session: after leadFollowupDelayMs,
// re-notify the client's destinations so they can chase it up. Skips leads
// that already converted in the meantime (checked at send time, not just at
// schedule time, since the delay can be hours).
function scheduleLeadFollowup({ store, env, client, leadId, delayMs }) {
  const timer = setTimeout(async () => {
    const current = store.getRecord("leads", leadId);
    if (!current || current.convertedAt || current.followupStatus !== "scheduled") return;
    await notify({ env, client, kind: "lead_followup", record: current });
    await store.updateRecord("leads", leadId, { followupStatus: "sent", followupSentAt: new Date().toISOString() });
  }, delayMs);
  if (typeof timer.unref === "function") timer.unref();
  return timer;
}

export async function createApp({ store = new JsonStore(dataDir), env = runtimeEnv } = {}) {
  await store.init();
  return createServer(async (req, res) => {
    const url = new URL(req.url, `http://${req.headers.host || "localhost"}`);
    try {
      if (req.method === "OPTIONS") {
        res.writeHead(204, { ...corsHeaders(req), "Access-Control-Allow-Headers": "Content-Type, Authorization", "Access-Control-Allow-Methods": "GET, POST, PUT, OPTIONS", "Access-Control-Max-Age": "86400" });
        return res.end();
      }

      if (req.method === "GET" && url.pathname === "/api/health") return json(res, 200, { ok: true, service: "ai-website-assistant", version: "0.1.0" });

      if (req.method === "GET" && url.pathname === "/api/public/config") {
        const client = store.resolveClient({ publicKey: url.searchParams.get("clientKey"), host: requestHost(req, url.searchParams.get("host")) });
        if (!client) return json(res, 404, { error: "Client profile was not found for this website." }, corsHeaders(req));
        return json(res, 200, { client: store.publicClient(client) }, corsHeaders(req));
      }

      if (req.method === "POST" && url.pathname === "/api/public/owner-dashboard-access") {
        const input = await bodyJson(req);
        const client = store.resolveClient({ publicKey: input.clientKey, host: requestHost(req, input.host) });
        if (!client) return json(res, 404, { error: "Client profile was not found for this website." }, corsHeaders(req));
        if (!ownerConsoleActivated(client)) return json(res, 403, { error: "Owner dashboard is available after assistant activation only." }, corsHeaders(req));
        const password = cleanText(input.password, 512, true);
        if (!ownerPasswordAuthorized(password, env, client.id)) return json(res, 401, { error: "Owner password was not accepted." }, corsHeaders(req));
        return json(res, 200, { dashboardUrl: `/owner?tenant=${encodeURIComponent(client.id)}` }, corsHeaders(req));
      }

      if (req.method === "POST" && url.pathname === "/api/public/chat") {
        const input = await bodyJson(req);
        const client = store.resolveClient({ publicKey: input.clientKey, host: requestHost(req, input.host) });
        if (!client) return json(res, 404, { error: "Client profile was not found for this website." }, corsHeaders(req));
        const message = cleanText(input.message, 2000, true);
        const history = Array.isArray(input.history) ? input.history.slice(-8) : [];
        let reply;
        try { reply = await createAssistantReply({ client, message, history, env }); }
        catch { reply = { text: "I’m having trouble reaching the answer service. I can still help you contact the team.", sources: [], action: client.enabledModules.includes("contact") ? { type: "contact", label: `Call ${client.contact.telephone}`, url: `tel:${client.contact.telephone.replace(/\s/g, "")}` } : null }; }
        await store.appendRecord("conversations", { clientId: client.id, sessionId: cleanText(input.sessionId, 100), pageUrl: cleanText(input.pageUrl, 500), message, reply: reply.text, mode: client.status });
        return json(res, 200, { reply, mode: client.status }, corsHeaders(req));
      }

      if (req.method === "POST" && url.pathname === "/api/public/preview-responses") {
        const input = await bodyJson(req);
        const client = store.resolveClient({ publicKey: input.clientKey, host: requestHost(req, input.host) });
        if (!client) return json(res, 404, { error: "Client profile was not found for this website." }, corsHeaders(req));
        const action = cleanText(input.action, 80, true);
        const allowedActions = new Set(["discuss_activation", "request_callback", "close_preview"]);
        if (!allowedActions.has(action)) throw Object.assign(new Error("Choose a valid preview response."), { status: 400 });
        const labels = { discuss_activation: "discuss activation", request_callback: "arrange callback", close_preview: "close preview" };
        const record = await store.appendRecord("previewResponses", {
          clientId: client.id, businessName: client.businessName, action, summary: `${client.businessName} response - ${labels[action]}`,
          pageUrl: cleanText(input.pageUrl, 500), sessionId: cleanText(input.sessionId, 100), simulated: client.status === "demo"
        });
        await writeResponseLedger({ env, record });
        return json(res, 201, { accepted: true, durable: true, record: { id: record.id, action: record.action, createdAt: record.createdAt }, simulated: record.simulated }, corsHeaders(req));
      }

      if (req.method === "POST" && ["/api/public/leads", "/api/public/callbacks"].includes(url.pathname)) {
        const input = await bodyJson(req);
        const client = store.resolveClient({ publicKey: input.clientKey, host: requestHost(req, input.host) });
        if (!client) return json(res, 404, { error: "Client profile was not found for this website." }, corsHeaders(req));
        const isLead = url.pathname.endsWith("leads");
        const requiredModule = isLead ? "leadCapture" : "callback";
        if (!client.enabledModules.includes(requiredModule)) return json(res, 403, { error: "This module is not enabled." }, corsHeaders(req));
        let record = await store.appendRecord(isLead ? "leads" : "callbacks", {
          clientId: client.id,
          name: cleanText(input.name, 120, true),
          telephone: cleanText(input.telephone, 40, true),
          email: cleanText(input.email, 160),
          preferredTime: cleanText(input.preferredTime, 120),
          service: cleanText(input.service, 160),
          reason: cleanText(input.reason || input.notes, 1000),
          simulated: client.status === "demo",
          convertedAt: null,
          convertedVia: null,
          followupStatus: "none",
          followupScheduledAt: null,
          followupSentAt: null
        });
        const notification = await notify({ env, client, kind: isLead ? "lead" : "callback", record });
        if (isLead && client.enabledModules.includes("leadFollowup")) {
          record = await store.updateRecord("leads", record.id, { followupStatus: "scheduled", followupScheduledAt: new Date().toISOString() });
          scheduleLeadFollowup({ store, env, client, leadId: record.id, delayMs: client.leadFollowupDelayMs });
        }
        return json(res, 201, { accepted: true, simulated: record.simulated, notification }, corsHeaders(req));
      }

      if (req.method === "POST" && url.pathname === "/api/public/events") {
        // Batched, first-party visitor analytics. Fire-and-forget from the page
        // (navigator.sendBeacon), so we always answer 202 and never block.
        const input = await bodyJson(req, 32 * 1024);
        const client = store.resolveClient({ publicKey: input.clientKey, host: requestHost(req, input.host) });
        if (!client) return json(res, 404, { error: "Client profile was not found for this website." }, corsHeaders(req));
        // Per-site on/off switch (owner-controlled). When off, accept-and-drop.
        if (client.analyticsEnabled === false) return json(res, 202, { accepted: true, stored: 0, disabled: true }, corsHeaders(req));
        const sessionId = cleanText(input.sessionId, 100);
        const rawEvents = Array.isArray(input.events) ? input.events.slice(0, 50) : [];
        const events = rawEvents
          .filter((event) => event && ALLOWED_EVENT_TYPES.has(String(event.type)))
          .map((event) => sanitizeEvent(event, { clientId: client.id, sessionId }));
        if (events.length) await store.appendRecords("events", events);
        return json(res, 202, { accepted: true, stored: events.length }, corsHeaders(req));
      }

      const demoMatch = url.pathname.match(/^\/api\/public\/demo\/(booking|payment|email|crm)$/);
      if (req.method === "POST" && demoMatch) {
        const workflow = demoMatch[1];
        const input = await bodyJson(req);
        const client = store.resolveClient({ publicKey: input.clientKey, host: requestHost(req, input.host) });
        if (!client) return json(res, 404, { error: "Client profile was not found for this website." }, corsHeaders(req));
        if (client.status !== "demo") return json(res, 403, { error: "Simulated workflows are available only in demo mode." }, corsHeaders(req));
        const modules = { booking: "demoBooking", payment: "demoPayment", email: "demoEmail", crm: "demoCrm" };
        if (!client.enabledModules.includes(modules[workflow])) return json(res, 403, { error: "This demo workflow is not enabled." }, corsHeaders(req));

        const config = client.demoWorkflows || {};
        let record;
        if (workflow === "booking") {
          const service = cleanText(input.service, 160, true);
          const slot = cleanText(input.slot, 120, true);
          const serviceConfig = (config.booking?.services || []).find((item) => item.name === service);
          if (!serviceConfig || !(config.booking?.slots || []).includes(slot)) throw Object.assign(new Error("Choose one of the seeded demo services and slots."), { status: 400 });
          record = await store.appendRecord("bookings", {
            clientId: client.id, reference: demoReference("BOOK"), name: cleanText(input.name, 120, true),
            telephone: cleanText(input.telephone, 40, true), email: cleanText(input.email, 160), service, slot,
            amount: serviceConfig.price, currency: config.payment?.currency || "GBP", status: "reserved", simulated: true
          });
        } else if (workflow === "payment") {
          const service = cleanText(input.service, 160, true);
          const serviceConfig = (config.booking?.services || []).find((item) => item.name === service);
          if (!serviceConfig) throw Object.assign(new Error("Choose one of the seeded demo services."), { status: 400 });
          record = await store.appendRecord("payments", {
            clientId: client.id, reference: demoReference("PAY"), customerName: cleanText(input.customerName, 120, true),
            service, amount: serviceConfig.price, currency: config.payment?.currency || "GBP",
            cardLabel: config.payment?.testCardLabel || "Demo card", status: "approved", simulated: true
          });
        } else if (workflow === "email") {
          const email = cleanText(input.email, 160, true);
          if (!validEmail(email)) throw Object.assign(new Error("Enter a valid demo recipient email address."), { status: 400 });
          const subject = cleanText(input.subject, 160, true);
          if (!(config.email?.subjects || []).includes(subject)) throw Object.assign(new Error("Choose one of the seeded demo email subjects."), { status: 400 });
          record = await store.appendRecord("emails", {
            clientId: client.id, reference: demoReference("MAIL"), recipientName: cleanText(input.recipientName, 120, true),
            email, subject, message: cleanText(input.message, 1200, true), fromName: config.email?.fromName || client.businessName,
            status: "previewed_not_sent", simulated: true
          });
        } else {
          const email = cleanText(input.email, 160);
          const telephone = cleanText(input.telephone, 40);
          if (!email && !telephone) throw Object.assign(new Error("Add a demo email address or telephone number."), { status: 400 });
          if (email && !validEmail(email)) throw Object.assign(new Error("Enter a valid demo email address."), { status: 400 });
          const stage = cleanText(input.stage, 80, true);
          if (!(config.crm?.pipelineStages || []).includes(stage)) throw Object.assign(new Error("Choose one of the seeded demo CRM stages."), { status: 400 });
          record = await store.appendRecord("crmLeads", {
            clientId: client.id, reference: demoReference("CRM"), name: cleanText(input.name, 120, true), email, telephone,
            interest: cleanText(input.interest, 160, true), stage, status: "created_in_demo_pipeline", simulated: true
          });
        }
        return json(res, 201, { accepted: true, simulated: true, workflow, record }, corsHeaders(req));
      }

      const completeCallbackMatch = url.pathname.match(/^\/api\/owner\/callbacks\/([^/]+)\/complete$/);
      if (req.method === "POST" && completeCallbackMatch) {
        const client = store.getClientById(cleanText(url.searchParams.get("tenant"), 120, true));
        if (!client) return json(res, 404, { error: "Owner console was not found." });
        if (!ownerConsoleActivated(client)) return json(res, 403, { error: "Owner console is available after assistant activation only." });
        if (!ownerAuthorized(req, env, client.id)) return json(res, 401, { error: "Owner access is required." });
        const callbackId = cleanText(decodeURIComponent(completeCallbackMatch[1]), 120, true);
        const callback = (store.listRecords().callbacks || []).find((record) => record.id === callbackId && record.clientId === client.id);
        if (!callback) return json(res, 404, { error: "Callback activity was not found." });
        const record = await store.updateRecord("callbacks", callbackId, { handledAt: new Date().toISOString(), handledByOwner: true });
        return json(res, 200, { record, performance: ownerPerformance(Object.fromEntries(Object.entries(store.listRecords()).map(([type, entries]) => [type, entries.filter((entry) => entry.clientId === client.id)])), client) });
      }

      if (req.method === "GET" && url.pathname === "/api/owner/activity") {
        const client = store.getClientById(cleanText(url.searchParams.get("tenant"), 120, true));
        if (!client) return json(res, 404, { error: "Owner console was not found." });
        if (!ownerConsoleActivated(client)) return json(res, 403, { error: "Owner console is available after assistant activation only." });
        if (!ownerAuthorized(req, env, client.id)) return json(res, 401, { error: "Owner access is required." });
        const allRecords = store.listRecords();
        // Raw page-behaviour events are high-volume and not conversation-shaped,
        // so they're summarised separately (pageAnalytics) rather than dumped
        // into the per-type activity timeline below.
        const { events: clientEvents = [], ...recordTypesForTimeline } = Object.fromEntries(
          Object.entries(allRecords).map(([type, entries]) => [type, entries.filter((entry) => entry.clientId === client.id)])
        );
        const records = recordTypesForTimeline;
        const summary = Object.fromEntries(Object.entries(records).map(([type, entries]) => [type, entries.length]));
        return json(res, 200, {
          owner: { id: client.id, businessName: client.businessName, status: client.status, enabledModules: client.enabledModules, reportingVocabulary: client.ownerReporting?.vocabulary || {} },
          records, summary, performance: ownerPerformance(records, client),
          pageAnalytics: pageAnalyticsSummary(clientEvents)
        });
      }

      if (url.pathname.startsWith("/api/admin/")) {
        if (!adminAuthorized(req, env)) return json(res, 401, { error: "Administrator authorization is required." });
        if (req.method === "GET" && url.pathname === "/api/admin/clients") return json(res, 200, { clients: store.listClients() });
        if (req.method === "GET" && url.pathname === "/api/admin/records") return json(res, 200, { records: store.listRecords() });
        if (req.method === "POST" && url.pathname === "/api/admin/clients") return json(res, 201, { client: await store.createClient(await bodyJson(req)) });
        const duplicateMatch = url.pathname.match(/^\/api\/admin\/clients\/([^/]+)\/duplicate$/);
        if (req.method === "POST" && duplicateMatch) {
          const client = await store.duplicateClient(decodeURIComponent(duplicateMatch[1]));
          return client ? json(res, 201, { client }) : json(res, 404, { error: "Client not found." });
        }
        const updateMatch = url.pathname.match(/^\/api\/admin\/clients\/([^/]+)$/);
        if (req.method === "PUT" && updateMatch) {
          const client = await store.updateClient(decodeURIComponent(updateMatch[1]), await bodyJson(req));
          return client ? json(res, 200, { client }) : json(res, 404, { error: "Client not found." });
        }
        const convertMatch = url.pathname.match(/^\/api\/admin\/leads\/([^/]+)\/convert$/);
        if (req.method === "POST" && convertMatch) {
          const leadId = decodeURIComponent(convertMatch[1]);
          const lead = store.getRecord("leads", leadId);
          if (!lead) return json(res, 404, { error: "Lead not found." });
          if (lead.convertedAt) return json(res, 200, { lead });
          const convertedVia = lead.followupStatus === "sent" ? "after_followup" : "same_session";
          const updated = await store.updateRecord("leads", leadId, { convertedAt: new Date().toISOString(), convertedVia });
          return json(res, 200, { lead: updated });
        }
        if (req.method === "GET" && url.pathname === "/api/admin/roi") {
          const clientId = url.searchParams.get("clientId");
          const client = clientId ? store.getClientById(clientId) : null;
          if (!client) return json(res, 404, { error: "Client not found." });
          const leads = store.listRecords().leads.filter((item) => item.clientId === clientId);
          const totalLeads = leads.length;
          const followupsSent = leads.filter((item) => item.followupStatus === "sent").length;
          const converted = leads.filter((item) => item.convertedAt).length;
          const convertedSameSession = leads.filter((item) => item.convertedVia === "same_session").length;
          const convertedAfterFollowup = leads.filter((item) => item.convertedVia === "after_followup").length;
          const recoveryRate = followupsSent ? convertedAfterFollowup / followupsSent : 0;
          const estimatedRecoveredRevenue = convertedAfterFollowup * client.averageJobValue;
          return json(res, 200, {
            clientId, businessName: client.businessName, averageJobValue: client.averageJobValue,
            totalLeads, followupsSent, converted, convertedSameSession, convertedAfterFollowup,
            recoveryRate, estimatedRecoveredRevenue
          });
        }
      }

      if (req.method === "GET") return serveStatic(url.pathname, res);
      return json(res, 404, { error: "Not found." });
    } catch (error) {
      return json(res, error.status || 500, { error: error.status ? error.message : "The service could not complete this request." });
    }
  });
}

async function serveStatic(pathname, res) {
  const routes = { "/": "index.html", "/admin": "admin.html", "/owner": "owner.html", "/widget.js": "widget.js" };
  const relative = routes[pathname] || pathname.replace(/^\//, "");
  const file = path.resolve(publicDir, relative);
  if (!file.startsWith(`${publicDir}${path.sep}`)) return json(res, 403, { error: "Forbidden." });
  try {
    const body = await readFile(file);
    const headers = { "Content-Type": MIME[path.extname(file)] || "application/octet-stream", "X-Content-Type-Options": "nosniff", "Referrer-Policy": "strict-origin-when-cross-origin" };
    if (path.basename(file) === "widget.js") headers["Cache-Control"] = "public, max-age=300";
    res.writeHead(200, headers);
    res.end(body);
  } catch { json(res, 404, { error: "Not found." }); }
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const app = await createApp();
  const port = Number(runtimeEnv.PORT || 4310);
  const host = runtimeEnv.HOST || "127.0.0.1";
  app.listen(port, host, () => console.log(`AI Website Assistant running at http://${host}:${port}`));
}

function loadEnvironment(file) {
  const loaded = { ...process.env };
  try {
    for (const line of readFileSync(file, "utf8").split(/\r?\n/)) {
      const match = line.match(/^\s*([A-Z_][A-Z0-9_]*)\s*=\s*(.*)\s*$/i);
      if (!match || loaded[match[1]] !== undefined) continue;
      loaded[match[1]] = match[2].replace(/^(['"])(.*)\1$/, "$2");
    }
  } catch { /* The environment file is optional. */ }
  loaded.ADMIN_TOKEN ||= "change-me-before-live-use";
  return loaded;
}
