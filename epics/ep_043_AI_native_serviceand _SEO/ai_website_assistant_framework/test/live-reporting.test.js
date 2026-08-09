import assert from "node:assert/strict";
import { mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { createApp } from "../src/server.js";
import { JsonStore } from "../src/store.js";

const frameworkRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

// Reads Server-Sent Events off a fetch Response body, yielding one parsed
// JSON payload per "data: ..." frame as they arrive.
async function* readSseEvents(response) {
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  while (true) {
    const { value, done } = await reader.read();
    if (done) return;
    buffer += decoder.decode(value, { stream: true });
    let boundary;
    while ((boundary = buffer.indexOf("\n\n")) >= 0) {
      const frame = buffer.slice(0, boundary);
      buffer = buffer.slice(boundary + 2);
      const line = frame.split("\n").find((item) => item.startsWith("data: "));
      if (line) yield JSON.parse(line.slice(6));
    }
  }
}

test("owner reporting stream: initial snapshot on connect, live push on new events, no push for other tenants", async (t) => {
  let closeServer;
  const temporary = await mkdtemp(path.join(os.tmpdir(), "live-reporting-"));
  await writeFile(path.join(temporary, "clients.json"), await readFile(path.join(frameworkRoot, "data", "clients.json")));
  await writeFile(path.join(temporary, "records.json"), JSON.stringify({
    conversations: [], leads: [], callbacks: [], bookings: [], payments: [], emails: [], crmLeads: [], events: [], questionFollowups: []
  }));
  const server = await createApp({
    store: new JsonStore(temporary),
    env: {
      ADMIN_TOKEN: "test-admin", OPENAI_API_KEY: "", NOTIFICATION_WEBHOOK_URL: "",
      BUSINESS_OWNER_TOKENS_JSON: JSON.stringify({ "the-tech-principle-local": "test-owner", "northstar-heating": "test-owner-north" })
    }
  });
  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  const base = `http://127.0.0.1:${server.address().port}`;
  closeServer = async () => { await new Promise((resolve) => server.close(resolve)); await rm(temporary, { recursive: true, force: true }); };
  // http.Server.close() waits for all open connections to end before its
  // callback fires — an SSE connection is deliberately kept open forever by
  // the server, so the stream must be aborted from the client side (and
  // that abort must be awaited) BEFORE server.close(), not just registered
  // as a same-priority after-hook, or close() — and the whole test process
  // — hangs waiting on a connection nothing ever told to end.
  const streamController = new AbortController();
  t.after(async () => {
    streamController.abort();
    await new Promise((resolve) => setImmediate(resolve));
    await closeServer();
  });

  const streamResponse = await fetch(`${base}/api/owner/reporting/stream?tenant=the-tech-principle-local`, {
    headers: { Authorization: "Bearer test-owner" }, signal: streamController.signal
  });
  assert.equal(streamResponse.status, 200);
  assert.match(streamResponse.headers.get("content-type"), /text\/event-stream/);

  const events = readSseEvents(streamResponse);
  const initial = (await events.next()).value;
  assert.equal(initial.clientId, "the-tech-principle-local");
  assert.equal(initial.summary.events, 0, "no events yet at connect time");

  // A write for a DIFFERENT tenant must not push anything to this stream.
  const otherTenantWrite = await fetch(`${base}/api/public/events`, {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ clientKey: "demo_northstar", host: "localhost", sessionId: "s-north", events: [{ type: "pageview", path: "/" }] })
  });
  assert.equal(otherTenantWrite.status, 202);

  // The real write, for the tenant we're actually subscribed to.
  const write = await fetch(`${base}/api/public/events`, {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ clientKey: "thetechprinciple_local", host: "thetechprinciple.com", sessionId: "s1", events: [{ type: "pageview", path: "/" }] })
  });
  assert.equal(write.status, 202);

  const pushed = (await events.next()).value;
  assert.equal(pushed.clientId, "the-tech-principle-local");
  assert.equal(pushed.summary.events, 1, "the pushed snapshot reflects the new event, and only one — the other tenant's write did not leak in");

  const secondWrite = await fetch(`${base}/api/public/leads`, {
    method: "POST", headers: { "Content-Type": "application/json" },
    // reasonForVisit is required for this client (leadReasonOptions configured) — see test/lead-reason.test.js.
    body: JSON.stringify({ clientKey: "thetechprinciple_local", host: "thetechprinciple.com", name: "Priya", telephone: "07123456789", reasonForVisit: "ai automation" })
  });
  assert.equal(secondWrite.status, 201);
  const pushedAgain = (await events.next()).value;
  assert.equal(pushedAgain.summary.leads, 1);
});
