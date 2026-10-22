import { NextResponse } from "next/server";
import { requireAdminUserForApi } from "@/lib/auth/require";
import { canManageVerification } from "@/lib/verification/repository";
import { sendPreparedVerificationBatch } from "@/lib/verification/batches";

export async function POST(request: Request, { params }: { params: Promise<{ batchId: string }> }) {
  const user = await requireAdminUserForApi();
  if (user instanceof NextResponse) return user;
  if (!canManageVerification(user.role)) return NextResponse.json({ error: "Forbidden." }, { status: 403 });
  const { batchId } = await params;
  let body: { confirmed?: boolean } = {};
  try { body = await request.json(); } catch {}
  if (body.confirmed !== true) {
    return NextResponse.json({ error: "Explicit confirmation is required before sending this batch." }, { status: 400 });
  }
  try {
    return NextResponse.json(await sendPreparedVerificationBatch({ batchId, actorUserId: user.id }));
  } catch (error) {
    return NextResponse.json({ error: error instanceof Error ? error.message : "Unable to send verification batch." }, { status: 400 });
  }
}
