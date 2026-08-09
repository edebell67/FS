import assert from "node:assert/strict";
import { mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { createAssistantReply, deterministicReply, retrieveKnowledge } from "../src/assistant.js";
import { createApp } from "../src/server.js";
import { JsonStore } from "../src/store.js";

const frameworkRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

test("deterministicReply offers a researched email answer, once, for a genuine knowledge gap", () => {
  const client = { businessName: "Test Co", enabledModules: [], knowledge: [{ id: "k1", title: "Pricing", content: "Quotes start at £95." }] };
  const matched = deterministicReply(client, "how much does a quote cost", retrieveKnowledge(client, "how much does a quote cost"));
  assert.equal(matched.action, undefined, "a real knowledge match must not trigger the fallback");

  const gap = deterministicReply(client, "do you offer octopus farming consultancy", retrieveKnowledge(client, "do you offer octopus farming consultancy"));
  assert.equal(gap.action?.type, "question-followup");
  assert.match(gap.text, /researched.*email|email.*researched/i);
});

test("createAssistantReply skips the LLM entirely on a knowledge gap, even with an API key configured", async () => {
  const client = { businessName: "Test Co", enabledModules: [], knowledge: [] };
  let fetchCalled = false;
  const reply = await createAssistantReply({
    client, message: "what is your policy on interdimensional travel",
    env: { OPENAI_API_KEY: "sk-test" },
    fetchImpl: async () => { fetchCalled = true; throw new Error("should not be called"); }
  });
  assert.equal(fetchCalled, false, "the model must not be called when there is no knowledge to ground it");
  assert.equal(reply.action?.type, "question-followup");
});

test("question-followups: accumulate per session, notify once, resolve via owner console", async (t) => {
  const temporary = await mkdtemp(path.join(os.tmpdir(), "question-followups-"));
  await writeFile(path.join(temporary, "clients.json"), await readFile(path.join(frameworkRoot, "data", "clients.json")));
  await writeFile(path.join(temporary, "records.json"), JSON.stringify({
    conversations: [], leads: [], callbacks: [], bookings: [], payments: [], emails: [], crmLeads: [], events: [], questionFollowups: []
  }));

  // notify() calls the bare global fetch (env.fetchImpl exists only for the
  // separate response-ledger path), so a real webhook call count can only be
  // observed by patching the global for this test's lifetime.
  let webhookCalls = 0;
  const realFetch = globalThis.fetch;
  globalThis.fetch = async (url, options) => {
    if (url === "http://webhook.invalid/notify") { webhookCalls += 1; return { ok: true, status: 200, json: async () => ({}) }; }
    return realFetch(url, options);
  };

  const server = await createApp({
    store: new JsonStore(temporary),
    env: {
      ADMIN_TOKEN: "test-admin", OPENAI_API_KEY: "", NOTIFICATION_WEBHOOK_URL: "http://webhook.invalid/notify",
      BUSINESS_OWNER_TOKENS_JSON: JSON.stringify({ "the-tech-principle-local": "test-owner" })
    }
  });
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
    globalThis.fetch = realFetch;
  });

  const rejected = await request("/api/public/question-followups", { method: "POST", body: {
    clientKey: "thetechprinciple_local", host: "thetechprinciple.com", sessionId: "s1", email: "not-an-email", question: "What's your escrow policy?"
  } });
  assert.equal(rejected.status, 400);

  const first = await request("/api/public/question-followups", { method: "POST", body: {
    clientKey: "thetechprinciple_local", host: "thetechprinciple.com", sessionId: "s1", email: "visitor@example.com", question: "What's your escrow policy?"
  } });
  assert.equal(first.status, 201);
  assert.equal(first.body.record.questions.length, 1);
  assert.equal(first.body.record.status, "pending");

  const second = await request("/api/public/question-followups", { method: "POST", body: {
    clientKey: "thetechprinciple_local", host: "thetechprinciple.com", sessionId: "s1", email: "visitor@example.com", question: "Do you sign NDAs before a discovery call?"
  } });
  assert.equal(second.status, 200, "second question in the same session appends, it does not create a new record");
  assert.equal(second.body.record.id, first.body.record.id, "one record per session, not one per question");
  assert.equal(second.body.record.questions.length, 2);
  assert.equal(second.body.notification.reason, "already_notified", "no second notification for an accumulated question");
  assert.equal(webhookCalls, 1, "exactly one notification call across two accumulated questions");

  const otherSession = await request("/api/public/question-followups", { method: "POST", body: {
    clientKey: "thetechprinciple_local", host: "thetechprinciple.com", sessionId: "s2", email: "someone-else@example.com", question: "Do you build mobile apps?"
  } });
  assert.equal(otherSession.status, 201, "a different session gets its own record and its own notification");
  assert.equal(webhookCalls, 2);

  const list = await request("/api/owner/question-followups?tenant=the-tech-principle-local", { owner: true });
  assert.equal(list.status, 200);
  assert.equal(list.body.pending.length, 2);
  assert.equal(list.body.resolved.length, 0);
  const pendingRecordId = first.body.record.id;

  const unauthorized = await request(`/api/owner/question-followups/${pendingRecordId}/resolve?tenant=the-tech-principle-local`, { method: "PUT" });
  assert.equal(unauthorized.status, 401);

  const resolved = await request(`/api/owner/question-followups/${pendingRecordId}/resolve?tenant=the-tech-principle-local`, { method: "PUT", owner: true });
  assert.equal(resolved.status, 200);
  assert.equal(resolved.body.record.status, "resolved");
  assert.ok(resolved.body.record.resolvedAt);

  const listAfter = await request("/api/owner/question-followups?tenant=the-tech-principle-local", { owner: true });
  assert.equal(listAfter.body.pending.length, 1);
  assert.equal(listAfter.body.resolved.length, 1);
});
