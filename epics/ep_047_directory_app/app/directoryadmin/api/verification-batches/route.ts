import { NextResponse } from "next/server";
import { requireAdminUserForApi } from "@/lib/auth/require";
import { canManageVerification } from "@/lib/verification/repository";
import { prepareVerificationBatch } from "@/lib/verification/batches";

export async function POST(request: Request) {
  const user = await requireAdminUserForApi();
  if (user instanceof NextResponse) return user;
  if (!canManageVerification(user.role)) {
    return NextResponse.json({ error: "Forbidden." }, { status: 403 });
  }
  let body: { businessIds?: unknown; expiresInDays?: unknown; includePartial?: unknown };
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ error: "Invalid JSON." }, { status: 400 });
  }
  try {
    return NextResponse.json(await prepareVerificationBatch(
      body.businessIds, user.id, body.expiresInDays, body.includePartial === true,
    ));
  } catch (error) {
    return NextResponse.json({
      error: error instanceof Error ? error.message : "Unable to prepare verification batch.",
    }, { status: 400 });
  }
}
