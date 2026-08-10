import { NextResponse } from "next/server";
import { requireAdminUserForApi } from "@/lib/auth/require";
import { getBusinessByRef } from "@/lib/db/queries/directory";
import { canManageVerification, issueVerificationLink, revokeVerificationLink } from "@/lib/verification/repository";
import { verificationCapabilityUrl } from "@/lib/verification/urls";
import { prepareDeliveryPreview } from "@/lib/verification/delivery";

export async function POST(request: Request, { params }: { params: Promise<{ businessRef: string }> }) {
  const user = await requireAdminUserForApi();
  if (user instanceof NextResponse) return user;
  if (!canManageVerification(user.role)) return NextResponse.json({ error: "Forbidden." }, { status: 403 });
  const business = await getBusinessByRef((await params).businessRef);
  if (!business) return NextResponse.json({ error: "Not found." }, { status: 404 });
  let body: { expiresInDays?: number; recipientAddress?: string } = {};
  try { body = await request.json(); } catch {}
  try {
    const link = await issueVerificationLink(business.id, user.id, body.expiresInDays);
    const recipientAddress = String(body.recipientAddress ?? "").trim();
    if (!recipientAddress) {
      await revokeVerificationLink(link.id);
      return NextResponse.json({ error: "Recipient email is required." }, { status: 400 });
    }
    const preview = await prepareDeliveryPreview({
      verificationLinkId: link.id, recipientAddress, actorUserId: user.id,
      businessName: business.businessName,
      listingUrl: `${new URL(verificationCapabilityUrl(link.rawToken)).origin}/directory/business/${encodeURIComponent(business.slug)}`,
      rawToken: link.rawToken, expiresAt: link.expiresAt,
    });
    return NextResponse.json({
      url: verificationCapabilityUrl(link.rawToken), linkId: link.id,
      expiresAt: link.expiresAt.toISOString(), expiresInDays: link.expiresInDays,
      deliveryState: "prepared", deliveryId: preview.auditId,
      trackingKey: preview.trackingKey, from: preview.from,
      subject: preview.message.subject, text: preview.message.text,
      deliveryEnabled: preview.deliveryEnabled, policyReason: preview.policyReason,
    });
  } catch (error) {
    return NextResponse.json({ error: error instanceof Error ? error.message : "Unable to prepare link." }, { status: 400 });
  }
}

export async function DELETE(request: Request) {
  const user = await requireAdminUserForApi();
  if (user instanceof NextResponse) return user;
  if (!canManageVerification(user.role)) return NextResponse.json({ error: "Forbidden." }, { status: 403 });
  const linkId = new URL(request.url).searchParams.get("linkId");
  if (!linkId) return NextResponse.json({ error: "Missing link." }, { status: 400 });
  return NextResponse.json({ revoked: await revokeVerificationLink(linkId) });
}
