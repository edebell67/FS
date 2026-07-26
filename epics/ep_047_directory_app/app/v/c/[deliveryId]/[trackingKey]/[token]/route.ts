import { NextResponse } from "next/server";
import { recordTrackedEvent } from "@/lib/verification/delivery";
import { isValidRawToken } from "@/lib/verification/tokens";
import { verificationCapabilityUrl } from "@/lib/verification/urls";

export const dynamic = "force-dynamic";

export async function GET(_request: Request, { params }: {
  params: Promise<{ deliveryId: string; trackingKey: string; token: string }>;
}) {
  const { deliveryId, trackingKey, token } = await params;
  if (!isValidRawToken(token)) {
    return new NextResponse("Verification link unavailable.", { status: 404 });
  }
  await recordTrackedEvent({ deliveryId, trackingKey, rawToken: token, eventType: "clicked" });
  const response = NextResponse.redirect(verificationCapabilityUrl(token), 302);
  response.headers.set("Cache-Control", "no-store");
  response.headers.set("Referrer-Policy", "no-referrer");
  return response;
}
