import { NextResponse } from "next/server";
import { sql } from "drizzle-orm";
import { db } from "@/lib/db/client";
import { APP_VERSION } from "@/lib/app-version";

export const dynamic = "force-dynamic";

/** Read-only scope projection for the separate static News prototype. */
export async function GET() {
  const result = await db.execute(sql`SELECT
    (SELECT town_mode FROM public_directory_settings WHERE id='default') AS town_mode,
    (SELECT category_mode FROM public_directory_settings WHERE id='default') AS category_mode,
    COALESCE((SELECT json_agg(lower(trim(town))) FROM businesses b
      WHERE b.town IS NOT NULL AND NOT EXISTS (SELECT 1 FROM public_town_visibility v
        WHERE v.town_key=lower(trim(b.town)) AND v.is_enabled=false)), '[]'::json) AS towns,
    COALESCE((SELECT json_agg(lower(trim(category))) FROM businesses b
      WHERE b.category IS NOT NULL AND NOT EXISTS (SELECT 1 FROM public_category_visibility v
        WHERE v.category_key=lower(trim(b.category)) AND v.is_enabled=false)), '[]'::json) AS categories`);
  const row = (result as any).rows?.[0] ?? {};
  return NextResponse.json({ version: APP_VERSION, townMode: row.town_mode ?? "all", categoryMode: row.category_mode ?? "all", towns: [...new Set(row.towns ?? [])], categories: [...new Set(row.categories ?? [])] });
}
