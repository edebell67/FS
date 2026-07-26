import { NextResponse } from "next/server";
import { requireAdminUserForApi } from "@/lib/auth/require";
import { canManageVerification } from "@/lib/verification/repository";
import { sendPreparedDelivery } from "@/lib/verification/delivery";

export async function POST(request: Request) {
  const user = await requireAdminUserForApi();
  if (user instanceof NextResponse) return user;
  if (!canManageVerification(user.role)) {
    return NextResponse.json({ error: "Forbidden." }, { status: 403 });
  }
  let body: {
    deliveryId?: string; rawToken?: string; trackingKey?: string; confirmed?: boolean;
  } = {};
  try { body = await request.json(); } catch {}
  if (body.confirmed !== true) {
    return NextResponse.json(
      { error: "Explicit confirmation is required before sending." },
      { status: 400 },
    );
  }
  if (!body.deliveryId || !body.rawToken || !body.trackingKey) {
    return NextResponse.json({ error: "Prepared delivery proof is missing." }, { status: 400 });
  }
  try {
    const sent = await sendPreparedDelivery({
      deliveryId: body.deliveryId, rawToken: body.rawToken,
      trackingKey: body.trackingKey, actorUserId: user.id,
    });
    return NextResponse.json({
      deliveryState: sent.status, sentAt: sent.sentAt.toISOString(),
    });
  } catch (error) {
    return NextResponse.json({
      error: error instanceof Error ? error.message : "Unable to send verification email.",
    }, { status: 400 });
  }
}
