import { NextResponse } from "next/server";
import { sql } from "drizzle-orm";
import { db } from "@/lib/db/client";
import { APP_VERSION } from "@/lib/app-version";
import { publicScopeWhere } from "@/ep047_visibility_news/lib/public-scope";

export const dynamic = "force-dynamic";

export async function GET() {
  const result = await db.execute(sql`SELECT a.id, a.slug, a.headline, a.town AS place,
    '' AS postcode, COALESCE(MIN(c.category_label), 'Local news') AS topic,
    a.source_name AS source, a.source_url AS url, a.verified_update, a.local_reading,
    a.business_voices, to_char(a.published_at, 'YYYY-MM-DD') AS date, COALESCE(json_agg(json_build_object('key', c.category_key, 'label', c.category_label))
      FILTER (WHERE c.id IS NOT NULL), '[]'::json) AS categories
    FROM news_articles a LEFT JOIN news_article_categories c ON c.article_id=a.id
    WHERE a.status='published' AND EXISTS (SELECT 1 FROM businesses WHERE lower(trim(town))=lower(trim(a.town)) AND ${publicScopeWhere()})
    GROUP BY a.id ORDER BY a.published_at DESC NULLS LAST, a.created_at DESC`);
  return NextResponse.json({ version: APP_VERSION, stories: (result as any).rows ?? [] });
}
