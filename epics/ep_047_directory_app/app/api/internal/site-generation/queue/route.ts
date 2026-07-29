import { NextResponse } from "next/server";
import { requireInternalApiKey } from "@/lib/auth/require-internal-api";
import { getBusinessesAwaitingSiteGeneration } from "@/lib/verification/site-generation";

/** Called by the Render Cron Job to fetch the current generation queue. Read-only. */
export async function GET(request: Request) {
  const auth = requireInternalApiKey(request);
  if (auth) return auth;
  const businesses = await getBusinessesAwaitingSiteGeneration();
  return NextResponse.json({ businesses });
}
