import { createHash, randomBytes, timingSafeEqual } from "node:crypto";
import nodemailer from "nodemailer";
import type SMTPTransport from "nodemailer/lib/smtp-transport";
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
export type DeliveryMode = "disabled" | "smtp";

type DeliveryEnvironment = Partial<Record<
  | "VERIFICATION_DELIVERY_MODE" | "VERIFICATION_DELIVERY_APPROVED"
  | "VERIFICATION_RECIPIENT_ALLOWLIST" | "EMAIL_FROM"
  | "SMTP_HOST" | "SMTP_PORT" | "SMTP_SECURE" | "SMTP_USERNAME" | "SMTP_PASSWORD"
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
  const mode: DeliveryMode = env.VERIFICATION_DELIVERY_MODE === "smtp" ? "smtp" : "disabled";
  const approved = env.VERIFICATION_DELIVERY_APPROVED === "true";
  const configuredAllowlist = (env.VERIFICATION_RECIPIENT_ALLOWLIST ?? "")
    .split(",").map(normaliseAddress).filter(Boolean);
  const allowlistIsStrict =
    configuredAllowlist.length === 1 && configuredAllowlist[0] === INITIAL_ALLOWED_RECIPIENT;
  const recipientAllowed = Boolean(recipient) &&
    allowlistIsStrict && configuredAllowlist.includes(normaliseAddress(recipient!));
  const port = Number(env.SMTP_PORT);
  const senderValid = normaliseAddress(env.EMAIL_FROM ?? "") === VERIFICATION_FROM;
  const smtpConfigured = Boolean(
    env.SMTP_HOST?.trim() && Number.isInteger(port) && port > 0 && port <= 65535 &&
    env.SMTP_USERNAME?.trim() && env.SMTP_PASSWORD &&
    (env.SMTP_SECURE === "true" || env.SMTP_SECURE === "false"),
  );
  const publicOriginReady = env.NODE_ENV === "production";
  const reasons = [
    mode !== "smtp" && "Delivery mode is disabled.",
    !approved && "SMTP delivery has not been explicitly approved.",
    !senderValid && `EMAIL_FROM must be exactly ${VERIFICATION_FROM}.`,
    !smtpConfigured && "Approved SMTP configuration is incomplete.",
    !publicOriginReady && "Sending requires the canonical production origin.",
    !allowlistIsStrict && `Recipient allowlist must contain only ${INITIAL_ALLOWED_RECIPIENT}.`,
    recipient !== undefined && !recipientAllowed && "Recipient is not allowlisted.",
  ].filter(Boolean) as string[];
  return {
    mode, approved, sender: VERIFICATION_FROM, recipientAllowed,
    canSend: reasons.length === 0,
    reason: reasons[0] ?? "Approved single-recipient SMTP delivery is configured.",
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

export type MailTransport = {
  sendMail(message: {
    from: string; to: string; subject: string; text: string; html: string;
  }): Promise<{ messageId?: string; accepted?: Array<string | { address?: string }> }>;
};

export async function handoffVerificationEmail(input: {
  transport: MailTransport; recipientAddress: string;
  subject: string; text: string; html: string;
}) {
  const recipientAddress = normaliseAddress(input.recipientAddress);
  const result = await input.transport.sendMail({
    from: VERIFICATION_FROM, to: recipientAddress,
    subject: input.subject, text: input.text, html: input.html,
  });
  const accepted = (result.accepted ?? []).some((entry) =>
    normaliseAddress(typeof entry === "string" ? entry : entry.address ?? "") === recipientAddress,
  );
  if (!accepted) throw new Error("SMTP provider did not accept the allowlisted recipient.");
  return result;
}

function createApprovedTransport(env: DeliveryEnvironment): MailTransport {
  const options: SMTPTransport.Options = {
    host: env.SMTP_HOST!,
    port: Number(env.SMTP_PORT),
    secure: env.SMTP_SECURE === "true",
    auth: { user: env.SMTP_USERNAME!, pass: env.SMTP_PASSWORD! },
  };
  return nodemailer.createTransport(options);
}

export async function sendPreparedDelivery(input: {
  deliveryId: string; rawToken: string; trackingKey: string; actorUserId: string;
}, options: { env?: DeliveryEnvironment; transport?: MailTransport } = {}) {
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
    const transport = options.transport ?? createApprovedTransport(env);
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
    const reason = error instanceof Error ? error.message.slice(0, 500) : "SMTP handoff failed.";
    await db.transaction(async (tx) => {
      await tx.update(verificationDeliveries).set({
        status: "failed", failedAt: new Date(), failureReason: reason,
      }).where(eq(verificationDeliveries.id, record.id));
      await tx.insert(verificationDeliveryEvents).values({
        deliveryId: record.id, eventType: "failed", actorUserId: input.actorUserId,
        metadata: { reason },
      });
    });
    throw new Error("SMTP handoff failed; no sent status was recorded.");
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
