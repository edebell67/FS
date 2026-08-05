import { NextResponse } from "next/server";
import { requireInternalApiKey } from "@/lib/auth/require-internal-api";
import { getBusinessGenerationReadiness } from "@/lib/verification/site-generation";

export async function GET(request: Request) {
  const auth = await requireInternalApiKey(request);
  if (auth) return auth;

  const businessRef = new URL(request.url).searchParams.get("businessRef")?.trim();
  if (!businessRef) {
    return NextResponse.json({ error: "businessRef is required." }, { status: 400 });
  }

  const readiness = await getBusinessGenerationReadiness(businessRef);
  if (!readiness) {
    return NextResponse.json({ error: "Business not found." }, { status: 404 });
  }
  return NextResponse.json(readiness);
}
