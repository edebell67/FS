import assert from "node:assert/strict";
import { mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { createApp } from "../src/server.js";
import { JsonStore } from "../src/store.js";
import { deterministicReply, retrieveKnowledge } from "../src/assistant.js";

const frameworkRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const siteRoot = path.resolve(frameworkRoot, "..", "..", "ep_046_thetechprinciple", "site");

test("The Tech Principle local site resolves to its isolated anonymous tracking client", async () => {
  const html = await readFile(path.join(siteRoot, "index.html"), "utf8");
  assert.match(html, /analytics-embed\.js/);
  assert.match(html, /widget\.js/);
  assert.match(html, /data-client="thetechprinciple_local"/g);
  assert.match(html, /data-api-base="https:\/\/shared-website-assistant-api\.onrender\.com"/g);

  const store = new JsonStore(path.join(frameworkRoot, "data"));
  await store.init();
  const client = store.resolveClient({ publicKey: "thetechprinciple_local", host: "thetechprinciple.com" });
  assert.ok(client);
  assert.equal(client.id, "the-tech-principle-local");
  assert.equal(client.status, "live");
  assert.equal(client.analyticsEnabled, true);
  assert.ok(client.knowledge.length > 0, "production knowledge base should not be empty");
  const quickAnswerExpectations = [
    ["What services do you provide?", /Web design and rebuilds.*AI site assistants.*Local SEO and lead generation.*Trading and data products/s],
    ["Tell me about your business.", /independent technology studio.*diagnose.*build.*prove/s],
    ["How much do your services cost?", /scope each project around the work required.*clear estimate/s],
  ];
  for (const [prompt, expected] of quickAnswerExpectations) {
    const reply = deterministicReply(client, prompt, retrieveKnowledge(client, prompt));
    assert.match(reply.text, expected, `quick action should return its dedicated approved TTP answer: ${prompt}`);
  }
  const quoteReply = deterministicReply(client, "I would like a quote.", retrieveKnowledge(client, "I would like a quote."));
  assert.equal(quoteReply.action?.type, "lead");
  assert.ok(store.resolveClient({ publicKey: "thetechprinciple_local", host: "localhost" }), "local dev host should still resolve");
  assert.equal(store.resolveClient({ publicKey: "thetechprinciple_local", host: "unapproved.example" }), null);
  const ownerDashboard = await readFile(path.join(frameworkRoot, "public", "owner.js"), "utf8");
  assert.match(ownerDashboard, /tracking\?\.uniqueVisits/);
  assert.match(ownerDashboard, /tracking\?\.serviceViews/);
});

test("The Tech Principle events flow into owner reporting, service comparison, and promotion measurement", async (t) => {
  const temporary = await mkdtemp(path.join(os.tmpdir(), "thetechprinciple-tracking-"));
  await writeFile(path.join(temporary, "clients.json"), await readFile(path.join(frameworkRoot, "data", "clients.json")));
  await writeFile(path.join(temporary, "records.json"), JSON.stringify({
    conversations: [], leads: [], callbacks: [], bookings: [], payments: [], emails: [], crmLeads: [],
    events: [{ id: "historic-service-view", clientId: "the-tech-principle-local", sessionId: "previous-visit", type: "service_view", service: "Web design & rebuilds", path: "/", createdAt: new Date(Date.now() - 2 * 86400000).toISOString() }]
  }));
  const server = await createApp({ store: new JsonStore(temporary), env: {
    ADMIN_TOKEN: "test-admin", OPENAI_API_KEY: "", NOTIFICATION_WEBHOOK_URL: "",
    BUSINESS_OWNER_TOKENS_JSON: JSON.stringify({ "the-tech-principle-local": "test-owner" })
  } });
  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  const base = `http://127.0.0.1:${server.address().port}`;
  const request = async (route, { method = "GET", body, owner = false } = {}) => {
    const response = await fetch(`${base}${route}`, {
      method,
      headers: { ...(body ? { "Content-Type": "application/json" } : {}), ...(owner ? { Authorization: "Bearer test-owner" } : {}) },
      body: body ? JSON.stringify(body) : undefined
    });
    return { status: response.status, body: await response.json() };
  };
  t.after(async () => {
    await new Promise((resolve) => server.close(resolve));
    await rm(temporary, { recursive: true, force: true });
  });

  const captured = await request("/api/public/events", { method: "POST", body: {
    clientKey: "thetechprinciple_local", host: "localhost", sessionId: "current-visit",
    events: [
      { type: "pageview", path: "/", device: "desktop" },
      { type: "service_view", path: "/", service: "AI site assistants" },
      { type: "service_view", path: "/", service: "AI site assistants" },
      { type: "service_view", path: "/", service: "AI site assistants" },
      { type: "cta_click", path: "/", label: "Start a project" },
      { type: "page_exit", path: "/", dwellMs: 18000, scrollPct: 75 }
    ]
  } });
  assert.equal(captured.status, 202);
  assert.equal(captured.body.stored, 6);

  const reporting = await request("/api/owner/reporting?tenant=the-tech-principle-local", { owner: true });
  assert.equal(reporting.status, 200);
  assert.equal(reporting.body.pageAnalytics.uniqueVisits, 2);
  assert.equal(reporting.body.pageAnalytics.pageViews, 1);
  assert.deepEqual(reporting.body.pageAnalytics.serviceViews[0], ["AI site assistants", 3]);

  const comparison = await request("/api/owner/reporting/compare?tenant=the-tech-principle-local&days=7", { owner: true });
  assert.equal(comparison.status, 200);
  assert.equal(comparison.body.comparison.pageViews.today, 1);
  assert.ok(comparison.body.comparison.perService.some((item) => item.service === "AI site assistants" && item.views.today === 3));
  assert.equal(comparison.body.comparison.signals[0].service, "AI site assistants");

  const created = await request("/api/owner/promotions", { method: "POST", owner: true, body: {
    clientId: "the-tech-principle-local", valueLabel: "Discovery offer", description: "A short, owner-created local offer.", services: ["AI site assistants"], displayOn: ["website"], durationDays: 7
  } });
  assert.equal(created.status, 201);
  const promotionId = created.body.promotion.promotionId;
  const publicPromotions = await request("/api/public/promotions?tenant=the-tech-principle-local");
  assert.equal(publicPromotions.status, 200);
  assert.equal(publicPromotions.body.promotions[0].promotionId, promotionId);

  const measured = await request("/api/public/events", { method: "POST", body: {
    clientKey: "thetechprinciple_local", host: "localhost", sessionId: "promo-visit",
    events: [
      { type: "promotion_impression", path: "/", promotionId, service: "AI site assistants" },
      { type: "promotion_click", path: "/", promotionId, service: "AI site assistants" }
    ]
  } });
  assert.equal(measured.body.stored, 2);
  const effectiveness = await request(`/api/owner/reporting/promotion/${encodeURIComponent(promotionId)}?tenant=the-tech-principle-local`, { owner: true });
  assert.equal(effectiveness.status, 200);
  assert.equal(effectiveness.body.duringPromotion.impressions, 1);
  assert.equal(effectiveness.body.duringPromotion.clicks, 1);
});
