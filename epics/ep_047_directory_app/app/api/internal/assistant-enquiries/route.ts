/**
 * app/api/internal/assistant-enquiries/route.ts — sends authenticated The Tech Principle widget enquiries.
 *
 * VERSION HISTORY
 * v1.1.0 · 2026-08-12 · Uses a route-specific shared key so assistant delivery cannot broaden the existing internal API credential surface.
 * v1.0.0 · 2026-08-12 · Adds fixed-tenant Gmail delivery with authenticated server-to-server access and Gmail SENT readback so assistant success means provider handoff was verified.
 */

import { createHash, timingSafeEqual } from "node:crypto";
import { NextResponse } from "next/server";
import { createGmailApiTransport, VERIFICATION_FROM } from "@/lib/verification/delivery";
import { senderPhysicalAddress } from "@/lib/verification/email-template";

const TTP_TENANT = "the-tech-principle-local";
const TTP_INBOX = "edward.bell@thetechprinciple.com";

type Enquiry = {
  id?: unknown;
  createdAt?: unknown;
  name?: unknown;
  telephone?: unknown;
  email?: unknown;
  reasonForVisit?: unknown;
  service?: unknown;
  preferredTime?: unknown;
  reason?: unknown;
};

function text(value: unknown, maximum: number): string {
  return String(value ?? "").replace(/[\u0000-\u001f]/g, " ").trim().slice(0, maximum);
}

function validEmail(value: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

function messageFor(kind: string, enquiry: Enquiry) {
  const name = text(enquiry.name, 120);
  const telephone = text(enquiry.telephone, 40);
  if (!name || !telephone) throw new Error("An enquiry name and telephone are required.");
  const email = text(enquiry.email, 160);
  if (email && !validEmail(email)) throw new Error("The enquiry email is invalid.");
  const lines = [
    `New ${kind === "callback" ? "callback request" : "website enquiry"} from The Tech Principle website.`,
    "",
    `Name: ${name}`,
    `Telephone: ${telephone}`,
    email ? `Email: ${email}` : "Email: not supplied",
    text(enquiry.reasonForVisit, 80) ? `Reason for visit: ${text(enquiry.reasonForVisit, 80)}` : "",
    text(enquiry.service, 160) ? `Service: ${text(enquiry.service, 160)}` : "",
    text(enquiry.preferredTime, 120) ? `Preferred callback time: ${text(enquiry.preferredTime, 120)}` : "",
    text(enquiry.reason, 1000) ? `Notes: ${text(enquiry.reason, 1000)}` : "",
    "",
    `Reference: ${text(enquiry.id, 100)}`,
    `Received: ${text(enquiry.createdAt, 40)}`,
  ].filter(Boolean);
  const subject = `[TTP] New ${kind === "callback" ? "callback request" : "website enquiry"}`;
  const body = lines.join("\n");
  const address = senderPhysicalAddress();
  if (!address) throw new Error("A registered sender address is required before enquiry delivery.");
  const htmlBody = body.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]!);
  const html = `<!doctype html><html lang="en"><body style="margin:0;background:#f2f2ee;color:#111;font-family:Arial,Helvetica,sans-serif"><div style="max-width:620px;margin:0 auto;padding:24px"><div style="background:#111;color:#fff;padding:24px;font-size:22px;font-weight:700">The Tech Principle<div style="width:56px;height:4px;background:#d7f542;margin-top:12px"></div></div><div style="background:#fff;padding:28px;line-height:1.55"><pre style="font-family:Arial,Helvetica,sans-serif;white-space:pre-wrap;margin:0">${htmlBody}</pre></div><div style="background:#fff;border-top:1px solid #ddd;padding:20px;color:#50504b;font-size:12px;line-height:1.5"><strong style="color:#111">The Tech Principle</strong><br>${address.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]!)}</div></div></body></html>`;
  return { subject, text: body, html };
}

function authorisedAssistantRequest(request: Request): boolean {
  const configured = process.env.ASSISTANT_ENQUIRY_DELIVERY_KEY?.trim();
  const provided = request.headers.get("authorization")?.replace(/^Bearer\s+/i, "").trim() || "";
  if (!configured || !provided) return false;
  const actual = createHash("sha256").update(provided).digest();
  const expected = createHash("sha256").update(configured).digest();
  return actual.length === expected.length && timingSafeEqual(actual, expected);
}

export async function POST(request: Request) {
  if (!authorisedAssistantRequest(request)) return NextResponse.json({ error: "Not authenticated." }, { status: 401 });
  let input: { tenant?: unknown; kind?: unknown; record?: Enquiry } = {};
  try { input = await request.json(); } catch { return NextResponse.json({ error: "Request body must be valid JSON." }, { status: 400 }); }
  if (input.tenant !== TTP_TENANT || !input.record || !["lead", "callback"].includes(String(input.kind))) {
    return NextResponse.json({ error: "Unsupported assistant enquiry request." }, { status: 400 });
  }
  try {
    const message = messageFor(String(input.kind), input.record);
    const result = await createGmailApiTransport(process.env).sendMessage({
      from: VERIFICATION_FROM, to: TTP_INBOX, subject: message.subject, text: message.text, html: message.html,
    });
    return NextResponse.json({ accepted: true, providerMessageId: result.messageId, sentReadback: "SENT" }, { status: 201 });
  } catch (error) {
    return NextResponse.json({ error: error instanceof Error ? error.message : "Enquiry delivery failed." }, { status: 502 });
  }
}
