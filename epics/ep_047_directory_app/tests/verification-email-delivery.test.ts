import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import {
  createGmailApiTransport, getDeliveryPolicy, VERIFICATION_FROM,
  handoffVerificationEmail,
} from "../lib/verification/delivery";
import { renderVerificationEmail } from "../lib/verification/email-template";
import { businessListingUrl, trackingClickUrl, trackingPixelUrl } from "../lib/verification/urls";

const enabledEnvironment = {
  NODE_ENV: "production",
  VERIFICATION_DELIVERY_MODE: "gmail-api",
  VERIFICATION_DELIVERY_APPROVED: "true",
  GMAIL_OAUTH_CLIENT_ID: "test-client-id",
  GMAIL_OAUTH_CLIENT_SECRET: "test-client-secret",
  GMAIL_OAUTH_REFRESH_TOKEN: "test-refresh-token",
  VERIFICATION_SENDER_ADDRESS: "1 Example Street, London, E1 1AA",
};
const PROSPECT_EMAIL = "prospect@example.com";

test("Gmail API policy enables a verified business recipient and still fails closed for transport prerequisites", () => {
  assert.equal(getDeliveryPolicy(PROSPECT_EMAIL, enabledEnvironment).canSend, true);
  assert.equal(getDeliveryPolicy("", enabledEnvironment).canSend, false);
  assert.equal(getDeliveryPolicy(PROSPECT_EMAIL, {
    ...enabledEnvironment, GMAIL_OAUTH_REFRESH_TOKEN: "",
  }).canSend, false);
});

test("controlled sender handoff uses the fixed From identity and no network transport", async () => {
  const messages: Array<Record<string, string>> = [];
  const result = await handoffVerificationEmail({
    recipientAddress: PROSPECT_EMAIL,
    subject: "Test verification", text: "test", html: "<p>test</p>",
    transport: {
      async sendMessage(message) {
        messages.push(message);
        return { messageId: "fake-provider-id" };
      },
    },
  });
  assert.equal(result.messageId, "fake-provider-id");
  assert.equal(messages.length, 1);
  assert.equal(messages[0]?.from, VERIFICATION_FROM);
  assert.equal(messages[0]?.to, PROSPECT_EMAIL);
});

test("controlled handoff rejects a Gmail response without a message ID", async () => {
  await assert.rejects(() => handoffVerificationEmail({
    recipientAddress: PROSPECT_EMAIL,
    subject: "Test verification", text: "test", html: "<p>test</p>",
    transport: { async sendMessage() { return { messageId: "" }; } },
  }), /message ID/);
});

test("Gmail transport refreshes OAuth and sends an encoded fixed-identity message", async () => {
  const requests: Array<{ url: string; init?: RequestInit }> = [];
  const fakeFetch = async (url: string | URL | Request, init?: RequestInit) => {
    requests.push({ url: String(url), init });
    if (requests.length === 1) return Response.json({ access_token: "short-lived-access-token" });
    if (requests.length === 2) return Response.json({ emailAddress: VERIFICATION_FROM });
    if (requests.length === 3) return Response.json({ id: "gmail-message-id", threadId: "gmail-thread-id" });
    return Response.json({
      id: "gmail-message-id", labelIds: ["SENT"],
      payload: { headers: [{ name: "From", value: VERIFICATION_FROM }, { name: "To", value: PROSPECT_EMAIL }] },
    });
  };
  const transport = createGmailApiTransport(enabledEnvironment, fakeFetch as typeof fetch);
  const result = await transport.sendMessage({
    from: VERIFICATION_FROM,
    to: PROSPECT_EMAIL,
    subject: "Test verification ✓",
    text: "plain body",
    html: "<p>html body</p>",
  });
  assert.equal(result.messageId, "gmail-message-id");
  assert.equal(requests[0]?.url, "https://oauth2.googleapis.com/token");
  assert.equal(requests[1]?.url, "https://gmail.googleapis.com/gmail/v1/users/me/profile");
  assert.equal(requests[2]?.url,
    "https://gmail.googleapis.com/gmail/v1/users/me/messages/send");
  assert.match(String(requests[3]?.url), /gmail-message-id.*format=metadata/);
  assert.equal(requests[2]?.init?.headers &&
    (requests[2].init.headers as Record<string, string>).authorization,
    "Bearer short-lived-access-token");
  const tokenBody = requests[0]?.init?.body as URLSearchParams;
  assert.equal(tokenBody.get("refresh_token"), "test-refresh-token");
  const sendBody = JSON.parse(String(requests[2]?.init?.body)) as { raw: string };
  const raw = Buffer.from(sendBody.raw, "base64url").toString("utf8");
  assert.match(raw, new RegExp(`From: ${VERIFICATION_FROM}`));
  assert.match(raw, new RegExp(`To: ${PROSPECT_EMAIL}`));
  assert.match(raw, /Content-Type: multipart\/alternative/);
  assert.doesNotMatch(raw, /refresh-token|access-token|client-secret/);
});

test("Gmail transport fails closed and never includes provider bodies in errors", async () => {
  assert.throws(() => createGmailApiTransport({
    ...enabledEnvironment, GMAIL_OAUTH_CLIENT_SECRET: "",
  }), /configuration is incomplete/);
  const transport = createGmailApiTransport(enabledEnvironment, (async () =>
    new Response('{"error":"test-refresh-token"}', { status: 401 })) as typeof fetch);
  await assert.rejects(() => transport.sendMessage({
    from: VERIFICATION_FROM, to: PROSPECT_EMAIL,
    subject: "Test", text: "test", html: "<p>test</p>",
  }), (error: unknown) => {
    assert.equal(error instanceof Error && error.message, "Gmail OAuth token refresh failed.");
    return true;
  });
});

test("tracked URLs have a fixed-origin redirect destination and email labels no delivery claim", () => {
  const click = trackingClickUrl("delivery", "tracking", "capability", enabledEnvironment);
  const pixel = trackingPixelUrl("delivery", "tracking", enabledEnvironment);
  assert.equal(click, "https://thetechprinciple.com/v/c/delivery/tracking/capability");
  assert.equal(pixel, "https://thetechprinciple.com/v/o/delivery/tracking.gif");
  const listing = businessListingUrl("a-business", enabledEnvironment);
  assert.equal(listing, "https://thetechprinciple.com/directory/business/a-business");
  const email = renderVerificationEmail({
    businessName: "<Business>", verificationUrl: click, listingUrl: listing,
    trackingPixelUrl: pixel, expiresAt: new Date("2026-08-01T00:00:00Z"),
  });
  assert.match(email.html, /&lt;Business&gt;/);
  assert.match(email.html, /width="1"/);
  assert.doesNotMatch(email.text, /delivered/i);
  // The expiry must read as a date a person would write, never an ISO stamp.
  assert.match(email.text, /expires on 1 August 2026\./);
  assert.doesNotMatch(email.text, /\d{4}-\d{2}-\d{2}T/);
});

test("verification HTML uses the approved black-and-lime TTP shell without raw action URLs", () => {
  const email = renderVerificationEmail({
    businessName: "Example Ltd",
    verificationUrl: "https://thetechprinciple.com/verify/capability-token",
    listingUrl: "https://thetechprinciple.com/directory/business/example-ltd",
    expiresAt: new Date("2026-08-16T00:00:00Z"),
  });
  assert.match(email.html, /background:#080808/);
  assert.match(email.html, /background:#b6ff00;color:#080808/);
  assert.match(email.html, /Review and correct details/);
  assert.match(email.html, /View public listing/);
  assert.doesNotMatch(email.html, /prepared message as sent/i);
  assert.doesNotMatch(email.html, />https:\/\/thetechprinciple\.com\/verify/);
  assert.doesNotMatch(email.html, />https:\/\/thetechprinciple\.com\/directory/);
});

test("delivery remains fail-closed while the required sender address is unset", () => {
  const { VERIFICATION_SENDER_ADDRESS: _address, ...withoutAddress } = enabledEnvironment;
  assert.equal(getDeliveryPolicy(PROSPECT_EMAIL, withoutAddress).canSend, false);
  assert.equal(getDeliveryPolicy(PROSPECT_EMAIL, enabledEnvironment).canSend, true);
});

test("migration stores hashes and append-only event metadata, never raw capabilities", async () => {
  const sql = await readFile(
    new URL("../migrations/0008_verification_email_delivery.sql", import.meta.url), "utf8",
  );
  assert.match(sql, /tracking_key_hash text/i);
  assert.match(sql, /verification_delivery_events/i);
  assert.match(sql, /'prepared','sent','opened','clicked','completed','failed','revoked'/);
  assert.doesNotMatch(sql, /raw_token|tracking_key text/i);
});

test("forward repair migration restores every delivery-tracking column used by the business detail", async () => {
  const [sql, journal] = await Promise.all([
    readFile(new URL("../migrations/0009_repair_verification_delivery_tracking.sql", import.meta.url), "utf8"),
    readFile(new URL("../migrations/meta/_journal.json", import.meta.url), "utf8"),
  ]);
  assert.match(journal, /0009_repair_verification_delivery_tracking/);
  assert.match(sql, /ALTER TABLE verification_deliveries/i);
  for (const column of [
    "status", "delivery_mode", "tracking_key_hash", "handoff_started_at", "opened_at",
    "clicked_at", "completed_at", "revoked_at",
  ]) assert.match(sql, new RegExp(`ADD COLUMN IF NOT EXISTS ${column}\\b`, "i"));
});

test("high-water migration applies the delivery tracking table and columns", async () => {
  const [sql, journal] = await Promise.all([
    readFile(new URL("../migrations/0010_apply_delivery_tracking_schema.sql", import.meta.url), "utf8"),
    readFile(new URL("../migrations/meta/_journal.json", import.meta.url), "utf8"),
  ]);
  assert.match(journal, /0010_apply_delivery_tracking_schema/);
  assert.match(sql, /tracking_key_hash text/i);
  assert.match(sql, /CREATE TABLE IF NOT EXISTS verification_delivery_events/i);
});

test("business-detail delivery lookup reads only its required durable status", async () => {
  const repository = await readFile(new URL("../lib/verification/repository.ts", import.meta.url), "utf8");
  const lookup = repository.slice(
    repository.indexOf("export async function getLatestDeliveryForBusiness"),
    repository.indexOf("export async function approveClaim"),
  );
  assert.match(lookup, /status: verificationDeliveries\.status/);
  assert.doesNotMatch(lookup, /verificationDeliveries\.(?:openedAt|clickedAt|completedAt|revokedAt|handoffStartedAt)/);
});

test("send endpoint requires explicit confirmation and tracking redirect is fixed", async () => {
  const sendRoute = await readFile(new URL(
    "../app/directoryadmin/api/businesses/[businessRef]/verification-email/route.ts",
    import.meta.url,
  ), "utf8");
  const clickRoute = await readFile(new URL(
    "../app/v/c/[deliveryId]/[trackingKey]/[token]/route.ts",
    import.meta.url,
  ), "utf8");
  assert.match(sendRoute, /body\.confirmed !== true/);
  assert.match(sendRoute, /canManageVerification\(user\.role\)/);
  assert.match(clickRoute, /verificationCapabilityUrl\(token\)/);
  assert.doesNotMatch(clickRoute, /searchParams\.get\(["'](?:url|redirect|next)/);
});
