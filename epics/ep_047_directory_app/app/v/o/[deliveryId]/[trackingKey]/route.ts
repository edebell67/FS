import { recordTrackedEvent } from "@/lib/verification/delivery";

export const dynamic = "force-dynamic";
const PIXEL = Buffer.from(
  "R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=",
  "base64",
);

export async function GET(_request: Request, { params }: {
  params: Promise<{ deliveryId: string; trackingKey: string }>;
}) {
  const { deliveryId, trackingKey: keyWithSuffix } = await params;
  const trackingKey = keyWithSuffix.endsWith(".gif")
    ? keyWithSuffix.slice(0, -4) : keyWithSuffix;
  await recordTrackedEvent({ deliveryId, trackingKey, eventType: "opened" });
  return new Response(PIXEL, {
    headers: {
      "Content-Type": "image/gif",
      "Content-Length": String(PIXEL.length),
      "Cache-Control": "no-store, private",
      "Referrer-Policy": "no-referrer",
      "X-Content-Type-Options": "nosniff",
    },
  });
}
