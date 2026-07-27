import { createHash, randomBytes, timingSafeEqual } from "node:crypto";
import { and, eq, isNull } from "drizzle-orm";
import { db } from "@/lib/db/client";
import {
  verificationDeliveries,
  verificationDeliveryEvents,
  verificationLinks,
  businesses,
} from "@/lib/db/schema";
import { VERIFICATION_TEMPLATE_VERSION, renderVerificationEmail } from "./email-template";
import { isValidRawToken, hashVerificationToken } from "./tokens";
import { trackingClickUrl, trackingPixelUrl } from "./urls";

export const VERIFICATION_FROM = "edward.bell@thetechprinciple.com";
export const INITIAL_ALLOWED_RECIPIENT = "edebell@gmail.com";
export type DeliveryMode = "disabled" | "gmail-api";

export type DeliveryEnvironment = Partial<Record<
  | "VERIFICATION_DELIVERY_MODE" | "VERIFICATION_DELIVERY_APPROVED"
  | "VERIFICATION_RECIPIENT_ALLOWLIST"
  | "GMAIL_OAUTH_CLIENT_ID" | "GMAIL_OAUTH_CLIENT_SECRET" | "GMAIL_OAUTH_REFRESH_TOKEN"
  | "NODE_ENV" | "NEXT_PUBLIC_SITE_URL",
  string | undefined
>>;

function normaliseAddress(value: string): string {
  return value.trim().toLowerCase();
}

export function getDeliveryPolicy(
  recipientOrEnv?: string | DeliveryEnvironment,
  providedEnv: DeliveryEnvironment = process.env,
) {
  const recipient = typeof recipientOrEnv === "string" ? recipientOrEnv : undefined;
  const env = typeof recipientOrEnv === "object" ? recipientOrEnv : providedEnv;
  const mode: DeliveryMode =
    env.VERIFICATION_DELIVERY_MODE === "gmail-api" ? "gmail-api" : "disabled";
  const approved = env.VERIFICATION_DELIVERY_APPROVED === "true";
  const configuredAllowlist = (env.VERIFICATION_RECIPIENT_ALLOWLIST ?? "")
    .split(",").map(normaliseAddress).filter(Boolean);
  const allowlistIsStrict =
    configuredAllowlist.length === 1 && configuredAllowlist[0] === INITIAL_ALLOWED_RECIPIENT;
  const recipientAllowed = Boolean(recipient) &&
    allowlistIsStrict && configuredAllowlist.includes(normaliseAddress(recipient!));
  const oauthConfigured = Boolean(
    env.GMAIL_OAUTH_CLIENT_ID?.trim() &&
    env.GMAIL_OAUTH_CLIENT_SECRET?.trim() &&
    env.GMAIL_OAUTH_REFRESH_TOKEN?.trim(),
  );
  const publicOriginReady = env.NODE_ENV === "production";
  const reasons = [
    mode !== "gmail-api" && "Delivery mode is disabled.",
    !approved && "Gmail API delivery has not been explicitly approved.",
    !oauthConfigured && "Gmail OAuth configuration is incomplete.",
    !publicOriginReady && "Sending requires the canonical production origin.",
    !allowlistIsStrict && `Recipient allowlist must contain only ${INITIAL_ALLOWED_RECIPIENT}.`,
    recipient !== undefined && !recipientAllowed && "Recipient is not allowlisted.",
  ].filter(Boolean) as string[];
  return {
    mode, approved, sender: VERIFICATION_FROM, recipientAllowed,
    canSend: reasons.length === 0,
    reason: reasons[0] ?? "Approved single-recipient Gmail API delivery is configured.",
  };
}

function hashTrackingKey(value: string): string {
  return createHash("sha256").update(value).digest("hex");
}

function safeHashEqual(raw: string, expectedHash: string): boolean {
  const actual = Buffer.from(hashTrackingKey(raw), "hex");
  const expected = Buffer.from(expectedHash, "hex");
  return actual.length === expected.length && timingSafeEqual(actual, expected);
}

export async function prepareDeliveryPreview(input: {
  verificationLinkId: string;
  recipientAddress: string;
  actorUserId: string;
  businessName: string;
  rawToken: string;
  expiresAt: Date;
}) {
  const recipientAddress = normaliseAddress(input.recipientAddress);
  const policy = getDeliveryPolicy(recipientAddress);
  const trackingKey = randomBytes(32).toString("base64url");
  const auditId = await db.transaction(async (tx) => {
    const [audit] = await tx.insert(verificationDeliveries).values({
      verificationLinkId: input.verificationLinkId, channel: "email",
      recipientAddress, templateVersion: VERIFICATION_TEMPLATE_VERSION,
      actorUserId: input.actorUserId, status: "prepared",
      deliveryMode: policy.mode, trackingKeyHash: hashTrackingKey(trackingKey),
    }).returning({ id: verificationDeliveries.id });
    if (!audit) throw new Error("Unable to record delivery preview.");
    await tx.insert(verificationDeliveryEvents).values({
      deliveryId: audit.id, eventType: "prepared", actorUserId: input.actorUserId,
      metadata: { channel: "email", templateVersion: VERIFICATION_TEMPLATE_VERSION },
    });
    return audit.id;
  });
  const clickUrl = trackingClickUrl(auditId, trackingKey, input.rawToken);
  const pixelUrl = trackingPixelUrl(auditId, trackingKey);
  const message = renderVerificationEmail({
    businessName: input.businessName, verificationUrl: clickUrl,
    trackingPixelUrl: pixelUrl, expiresAt: input.expiresAt,
  });
  return {
    auditId, trackingKey, message, from: VERIFICATION_FROM,
    deliveryEnabled: policy.canSend, policyReason: policy.reason,
  };
}

export type GmailTransport = {
  sendMessage(message: {
    from: string; to: string; subject: string; text: string; html: string;
  }): Promise<{ messageId: string }>;
};

export async function handoffVerificationEmail(input: {
  transport: GmailTransport; recipientAddress: string;
  subject: string; text: string; html: string;
}) {
  const recipientAddress = normaliseAddress(input.recipientAddress);
  if (recipientAddress !== INITIAL_ALLOWED_RECIPIENT) {
    throw new Error("Recipient is not allowlisted.");
  }
  const result = await input.transport.sendMessage({
    from: VERIFICATION_FROM, to: recipientAddress,
    subject: input.subject, text: input.text, html: input.html,
  });
  if (!result.messageId?.trim()) {
    throw new Error("Gmail API did not return a message ID.");
  }
  return result;
}

type Fetch = typeof fetch;

function encodeHeader(value: string): string {
  return `=?UTF-8?B?${Buffer.from(value, "utf8").toString("base64")}?=`;
}

function wrapBase64(value: string): string {
  return value.match(/.{1,76}/g)?.join("\r\n") ?? "";
}

function buildRawMessage(message: {
  from: string; to: string; subject: string; text: string; html: string;
}): string {
  const boundary = `ep047-${randomBytes(18).toString("hex")}`;
  const lines = [
    `From: ${message.from}`,
    `To: ${message.to}`,
    `Reply-To: ${message.from}`,
    `Date: ${new Date().toUTCString()}`,
    `Message-ID: <${randomBytes(18).toString("hex")}@thetechprinciple.com>`,
    `Subject: ${encodeHeader(message.subject)}`,
    "MIME-Version: 1.0",
    `Content-Type: multipart/alternative; boundary="${boundary}"`,
    "",
    `--${boundary}`,
    'Content-Type: text/plain; charset="UTF-8"',
    "Content-Transfer-Encoding: base64",
    "",
    wrapBase64(Buffer.from(message.text, "utf8").toString("base64")),
    `--${boundary}`,
    'Content-Type: text/html; charset="UTF-8"',
    "Content-Transfer-Encoding: base64",
    "",
    wrapBase64(Buffer.from(message.html, "utf8").toString("base64")),
    `--${boundary}--`,
    "",
  ];
  return Buffer.from(lines.join("\r\n"), "utf8").toString("base64url");
}

export function createGmailApiTransport(
  env: DeliveryEnvironment,
  fetchImpl: Fetch = fetch,
  allowedRecipients: string[] = [INITIAL_ALLOWED_RECIPIENT],
): GmailTransport {
  const clientId = env.GMAIL_OAUTH_CLIENT_ID?.trim();
  const clientSecret = env.GMAIL_OAUTH_CLIENT_SECRET?.trim();
  const refreshToken = env.GMAIL_OAUTH_REFRESH_TOKEN?.trim();
  if (!clientId || !clientSecret || !refreshToken) {
    throw new Error("Gmail OAuth configuration is incomplete.");
  }
  return {
    async sendMessage(message) {
      if (message.from !== VERIFICATION_FROM ||
          !allowedRecipients.includes(normaliseAddress(message.to))) {
        throw new Error("Gmail message violates the fixed sender or recipient policy.");
      }
      const tokenResponse = await fetchImpl("https://oauth2.googleapis.com/token", {
        method: "POST",
        headers: { "content-type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({
          client_id: clientId,
          client_secret: clientSecret,
          refresh_token: refreshToken,
          grant_type: "refresh_token",
        }),
      });
      if (!tokenResponse.ok) throw new Error("Gmail OAuth token refresh failed.");
      const tokenPayload = await tokenResponse.json() as { access_token?: unknown };
      if (typeof tokenPayload.access_token !== "string" || !tokenPayload.access_token) {
        throw new Error("Gmail OAuth token refresh returned no access token.");
      }
      const profileResponse = await fetchImpl("https://gmail.googleapis.com/gmail/v1/users/me/profile", {
        headers: { authorization: `Bearer ${tokenPayload.access_token}` },
      });
      if (!profileResponse.ok) throw new Error("Gmail profile verification failed.");
      const profile = await profileResponse.json() as { emailAddress?: unknown };
      if (typeof profile.emailAddress !== "string" || normaliseAddress(profile.emailAddress) !== normaliseAddress(VERIFICATION_FROM)) {
        throw new Error("Gmail OAuth account does not match the approved sender identity.");
      }
      const sendResponse = await fetchImpl(
        "https://gmail.googleapis.com/gmail/v1/users/me/messages/send",
        {
          method: "POST",
          headers: {
            authorization: `Bearer ${tokenPayload.access_token}`,
            "content-type": "application/json",
          },
          body: JSON.stringify({ raw: buildRawMessage(message) }),
        },
      );
      if (!sendResponse.ok) throw new Error("Gmail API message handoff failed.");
      const sendPayload = await sendResponse.json() as { id?: unknown };
      if (typeof sendPayload.id !== "string" || !sendPayload.id) {
        throw new Error("Gmail API did not return a message ID.");
      }
      const sentResponse = await fetchImpl(
        `https://gmail.googleapis.com/gmail/v1/users/me/messages/${encodeURIComponent(sendPayload.id)}?format=metadata&metadataHeaders=From&metadataHeaders=To`,
        { headers: { authorization: `Bearer ${tokenPayload.access_token}` } },
      );
      if (!sentResponse.ok) throw new Error("Gmail sent-message readback failed.");
      const sentMessage = await sentResponse.json() as {
        labelIds?: unknown; payload?: { headers?: Array<{ name?: unknown; value?: unknown }> };
      };
      const labels = Array.isArray(sentMessage.labelIds) ? sentMessage.labelIds : [];
      const headers = sentMessage.payload?.headers ?? [];
      const header = (name: string) => headers.find((item) => String(item.name).toLowerCase() === name)?.value;
      if (!labels.includes("SENT") || normaliseAddress(String(header("from") ?? "")) !== normaliseAddress(VERIFICATION_FROM) ||
          normaliseAddress(String(header("to") ?? "")) !== normaliseAddress(message.to)) {
        throw new Error("Gmail sent-message readback did not verify the required sender, recipient, and SENT label.");
      }
      return { messageId: sendPayload.id };
    },
  };
}

export async function sendPreparedDelivery(input: {
  deliveryId: string; rawToken: string; trackingKey: string; actorUserId: string;
}, options: { env?: DeliveryEnvironment; transport?: GmailTransport } = {}) {
  const env = options.env ?? process.env;
  if (!isValidRawToken(input.rawToken)) throw new Error("Invalid verification capability.");
  const [record] = await db.select({
    id: verificationDeliveries.id,
    recipientAddress: verificationDeliveries.recipientAddress,
    status: verificationDeliveries.status,
    trackingKeyHash: verificationDeliveries.trackingKeyHash,
    tokenHash: verificationLinks.tokenHash,
    expiresAt: verificationLinks.expiresAt,
    revokedAt: verificationLinks.revokedAt,
    businessName: businesses.businessName,
  }).from(verificationDeliveries)
    .innerJoin(verificationLinks, eq(verificationDeliveries.verificationLinkId, verificationLinks.id))
    .innerJoin(businesses, eq(verificationLinks.businessId, businesses.id))
    .where(and(
      eq(verificationDeliveries.id, input.deliveryId),
      eq(verificationDeliveries.actorUserId, input.actorUserId),
      isNull(verificationDeliveries.sentAt),
      isNull(verificationDeliveries.handoffStartedAt),
    )).limit(1);
  if (!record || record.status !== "prepared" || record.revokedAt) {
    throw new Error("Prepared delivery is unavailable.");
  }
  if (record.expiresAt <= new Date() ||
      record.tokenHash !== hashVerificationToken(input.rawToken) ||
      !safeHashEqual(input.trackingKey, record.trackingKeyHash)) {
    throw new Error("Prepared delivery confirmation is invalid or expired.");
  }
  const policy = getDeliveryPolicy(record.recipientAddress, env);
  if (!policy.canSend) throw new Error(policy.reason);
  const claimed = await db.update(verificationDeliveries).set({
    handoffStartedAt: new Date(),
  }).where(and(
    eq(verificationDeliveries.id, record.id),
    eq(verificationDeliveries.status, "prepared"),
    isNull(verificationDeliveries.handoffStartedAt),
  )).returning({ id: verificationDeliveries.id });
  if (!claimed.length) throw new Error("Prepared delivery is already being processed.");

  const clickUrl = trackingClickUrl(
    // The link ID is deliberately not needed for authorization; delivery UUID
    // is used by tracking. Retain the delivery ID in the public routes.
    input.deliveryId, input.trackingKey, input.rawToken, env,
  );
  const pixelUrl = trackingPixelUrl(input.deliveryId, input.trackingKey, env);
  const message = renderVerificationEmail({
    businessName: record.businessName, verificationUrl: clickUrl,
    trackingPixelUrl: pixelUrl, expiresAt: record.expiresAt,
  });
  try {
    const transport = options.transport ?? createGmailApiTransport(env);
    const result = await handoffVerificationEmail({
      transport, recipientAddress: record.recipientAddress,
      subject: message.subject, text: message.text, html: message.html,
    });
    const now = new Date();
    await db.transaction(async (tx) => {
      await tx.update(verificationDeliveries).set({
        status: "sent", sentAt: now, providerMessageId: result.messageId ?? null,
        failureReason: null, failedAt: null,
      }).where(and(eq(verificationDeliveries.id, record.id), isNull(verificationDeliveries.sentAt)));
      await tx.insert(verificationDeliveryEvents).values({
        deliveryId: record.id, eventType: "sent", actorUserId: input.actorUserId,
        metadata: { providerAccepted: true },
      });
    });
    return { status: "sent" as const, sentAt: now, providerMessageId: result.messageId ?? null };
  } catch (error) {
    const reason = error instanceof Error ? error.message.slice(0, 500) : "Gmail API handoff failed.";
    await db.transaction(async (tx) => {
      await tx.update(verificationDeliveries).set({
        status: "failed", failedAt: new Date(), failureReason: reason,
      }).where(eq(verificationDeliveries.id, record.id));
      await tx.insert(verificationDeliveryEvents).values({
        deliveryId: record.id, eventType: "failed", actorUserId: input.actorUserId,
        metadata: { reason },
      });
    });
    throw new Error("Gmail API handoff failed; no sent status was recorded.");
  }
}

export async function recordTrackedEvent(input: {
  deliveryId: string; trackingKey: string; eventType: "opened" | "clicked";
  rawToken?: string;
}) {
  const [record] = await db.select({
    id: verificationDeliveries.id, sentAt: verificationDeliveries.sentAt,
    revokedAt: verificationDeliveries.revokedAt, trackingKeyHash: verificationDeliveries.trackingKeyHash,
    openedAt: verificationDeliveries.openedAt, clickedAt: verificationDeliveries.clickedAt,
    status: verificationDeliveries.status, tokenHash: verificationLinks.tokenHash,
  }).from(verificationDeliveries)
    .innerJoin(verificationLinks, eq(verificationDeliveries.verificationLinkId, verificationLinks.id))
    .where(eq(verificationDeliveries.id, input.deliveryId)).limit(1);
  if (!record || !record.sentAt || record.revokedAt ||
      !safeHashEqual(input.trackingKey, record.trackingKeyHash) ||
      (input.eventType === "clicked" &&
        (!input.rawToken || hashVerificationToken(input.rawToken) !== record.tokenHash))) return false;
  const now = new Date();
  const first = input.eventType === "opened" ? !record.openedAt : !record.clickedAt;
  const terminal = record.status === "completed" || record.status === "revoked";
  await db.transaction(async (tx) => {
    await tx.update(verificationDeliveries).set(input.eventType === "opened"
      ? { openedAt: record.openedAt ?? now,
          status: terminal ? record.status : record.clickedAt ? "clicked" : "opened" }
      : { clickedAt: record.clickedAt ?? now,
          status: terminal ? record.status : "clicked" })
      .where(eq(verificationDeliveries.id, record.id));
    if (first) await tx.insert(verificationDeliveryEvents).values({
      deliveryId: record.id, eventType: input.eventType,
      metadata: { bestEffort: input.eventType === "opened" },
    });
  });
  return true;
}
