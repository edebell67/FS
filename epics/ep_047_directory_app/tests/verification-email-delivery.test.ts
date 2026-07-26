import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import {
  getDeliveryPolicy, INITIAL_ALLOWED_RECIPIENT, VERIFICATION_FROM,
  handoffVerificationEmail,
} from "../lib/verification/delivery";
import { renderVerificationEmail } from "../lib/verification/email-template";
import { trackingClickUrl, trackingPixelUrl } from "../lib/verification/urls";

const enabledEnvironment = {
  NODE_ENV: "production",
  VERIFICATION_DELIVERY_MODE: "smtp",
  VERIFICATION_DELIVERY_APPROVED: "true",
  VERIFICATION_RECIPIENT_ALLOWLIST: INITIAL_ALLOWED_RECIPIENT,
  EMAIL_FROM: VERIFICATION_FROM,
  SMTP_HOST: "smtp.approved.example",
  SMTP_PORT: "465",
  SMTP_SECURE: "true",
  SMTP_USERNAME: "approved-user",
  SMTP_PASSWORD: "test-only-password",
};

test("SMTP policy fails closed and enables only the exact initial recipient", () => {
  assert.equal(getDeliveryPolicy(INITIAL_ALLOWED_RECIPIENT, enabledEnvironment).canSend, true);
  assert.equal(getDeliveryPolicy("prospect@example.com", enabledEnvironment).canSend, false);
  assert.equal(getDeliveryPolicy(INITIAL_ALLOWED_RECIPIENT, {
    ...enabledEnvironment, EMAIL_FROM: "attacker@example.com",
  }).canSend, false);
  assert.equal(getDeliveryPolicy(INITIAL_ALLOWED_RECIPIENT, {
    ...enabledEnvironment, VERIFICATION_RECIPIENT_ALLOWLIST:
      `${INITIAL_ALLOWED_RECIPIENT},prospect@example.com`,
  }).canSend, false);
  assert.equal(getDeliveryPolicy(INITIAL_ALLOWED_RECIPIENT, {
    ...enabledEnvironment, SMTP_PASSWORD: "",
  }).canSend, false);
});

test("controlled sender handoff uses the fixed From identity and no network transport", async () => {
  const messages: Array<Record<string, string>> = [];
  const result = await handoffVerificationEmail({
    recipientAddress: INITIAL_ALLOWED_RECIPIENT,
    subject: "Test verification", text: "test", html: "<p>test</p>",
    transport: {
      async sendMail(message) {
        messages.push(message);
        return { messageId: "fake-provider-id", accepted: [INITIAL_ALLOWED_RECIPIENT] };
      },
    },
  });
  assert.equal(result.messageId, "fake-provider-id");
  assert.equal(messages.length, 1);
  assert.equal(messages[0]?.from, VERIFICATION_FROM);
  assert.equal(messages[0]?.to, INITIAL_ALLOWED_RECIPIENT);
});

test("controlled handoff rejects a provider response that did not accept the recipient", async () => {
  await assert.rejects(() => handoffVerificationEmail({
    recipientAddress: INITIAL_ALLOWED_RECIPIENT,
    subject: "Test verification", text: "test", html: "<p>test</p>",
    transport: { async sendMail() { return { accepted: [] }; } },
  }), /did not accept/);
});

test("tracked URLs have a fixed-origin redirect destination and email labels no delivery claim", () => {
  const click = trackingClickUrl("delivery", "tracking", "capability", enabledEnvironment);
  const pixel = trackingPixelUrl("delivery", "tracking", enabledEnvironment);
  assert.equal(click, "https://thetechprinciple.com/v/c/delivery/tracking/capability");
  assert.equal(pixel, "https://thetechprinciple.com/v/o/delivery/tracking.gif");
  const email = renderVerificationEmail({
    businessName: "<Business>", verificationUrl: click,
    trackingPixelUrl: pixel, expiresAt: new Date("2026-08-01T00:00:00Z"),
  });
  assert.match(email.html, /&lt;Business&gt;/);
  assert.match(email.html, /width="1"/);
  assert.doesNotMatch(email.text, /delivered/i);
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
