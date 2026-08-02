import { NextResponse } from "next/server";
import { validateNewsIntakeDelivery } from "@/lib/news-intake/request";
import { importNewsIntakeBatch } from "@/lib/news-intake/service";

export async function POST(request: Request) {
  const raw = await request.text();
  const delivery = validateNewsIntakeDelivery({
    raw,
    authorization: request.headers.get("authorization"),
    batchHash: request.headers.get("x-news-batch-hash"),
    configuredApiKey: process.env.NEWS_IMPORT_API_KEY,
  });
  if (!delivery.ok) return NextResponse.json({ error: delivery.error }, { status: delivery.status });

  try {
    const outcome = await importNewsIntakeBatch(delivery.batch, "api:news-intake");
    return NextResponse.json({ outcome });
  } catch {
    return NextResponse.json({ error: "Unable to process news intake batch." }, { status: 500 });
  }
}
