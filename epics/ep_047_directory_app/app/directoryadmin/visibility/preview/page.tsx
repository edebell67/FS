import Link from "next/link";
import { requireAdminUserForPage } from "@/lib/auth/require";
import { db } from "@/lib/db/client";
import { sql } from "drizzle-orm";

export const dynamic = "force-dynamic";

/**
 * Non-mutating logged-out preview: renders directory/town/category/news results the way an
 * anonymous visitor would see them under a hypothetical (not-yet-saved) town/category mode.
 * Individual town/category enable flags and business overrides are read from the live,
 * already-saved tables — only the two global mode toggles are hypothetical, taken from the
 * query string rather than public_directory_settings. This intentionally mirrors (does not
 * import) publicScopeWhere() in ep047_visibility_news/lib/public-scope.ts, because that
 * function always reads the *saved* mode from the database and has no parameterized form —
 * keeping this preview's predicate physically separate guarantees a bug here can never affect
 * the live public resolver, and vice versa.
 */
type Mode = "all" | "selected";
function parseMode(value: string | undefined, fallback: Mode): Mode {
  return value === "selected" ? "selected" : value === "all" ? "all" : fallback;
}

export default async function VisibilityPreviewPage({
  searchParams,
}: {
  searchParams: Promise<{ townMode?: string; categoryMode?: string }>;
}) {
  await requireAdminUserForPage("/directoryadmin/visibility/preview");
  const saved = await db.execute(sql`SELECT town_mode, category_mode FROM public_directory_settings WHERE id='default'`);
  const savedRow = (saved as any).rows?.[0] ?? { town_mode: "all", category_mode: "all" };
  const { townMode: qTown, categoryMode: qCategory } = await searchParams;
  const townMode = parseMode(qTown, savedRow.town_mode);
  const categoryMode = parseMode(qCategory, savedRow.category_mode);

  const scope = sql`(
    COALESCE((SELECT v.decision FROM public_business_visibility v WHERE v.business_id = b.id), 'inherit') = 'show'
    OR (
      COALESCE((SELECT v.decision FROM public_business_visibility v WHERE v.business_id = b.id), 'inherit') <> 'hide'
      AND (${townMode} = 'all' OR NOT EXISTS (SELECT 1 FROM public_town_visibility t WHERE t.town_key = lower(trim(b.town)) AND t.is_enabled = false))
      AND (${categoryMode} = 'all' OR NOT EXISTS (SELECT 1 FROM public_category_visibility c WHERE c.category_key = lower(trim(b.category)) AND c.is_enabled = false))
    )
  )`;

  const totals = await db.execute(sql`SELECT count(*)::int AS businesses,
    count(DISTINCT lower(trim(b.town)))::int AS towns, count(DISTINCT lower(trim(b.category)))::int AS categories
    FROM businesses b WHERE ${scope}`);
  const totalsRow = (totals as any).rows?.[0] ?? { businesses: 0, towns: 0, categories: 0 };

  const towns = await db.execute(sql`SELECT initcap(trim(b.town)) AS label, count(*)::int AS count
    FROM businesses b WHERE b.town IS NOT NULL AND trim(b.town) <> '' AND ${scope}
    GROUP BY initcap(trim(b.town)) ORDER BY label LIMIT 60`);

  const categories = await db.execute(sql`SELECT initcap(trim(b.category)) AS label, count(*)::int AS count
    FROM businesses b WHERE b.category IS NOT NULL AND trim(b.category) <> '' AND ${scope}
    GROUP BY initcap(trim(b.category)) ORDER BY label LIMIT 60`);

  const sample = await db.execute(sql`SELECT b.business_name, b.town, b.category
    FROM businesses b WHERE ${scope} ORDER BY b.business_name LIMIT 10`);

  const newsLink = await db.execute(sql`SELECT a.headline, a.town, a.slug
    FROM news_articles a WHERE a.status='published' AND a.duplicate_state='unique'
      AND EXISTS (SELECT 1 FROM businesses b WHERE lower(trim(b.town))=lower(trim(a.town)) AND ${scope})
    ORDER BY COALESCE(a.effective_story_date, a.published_at::date) DESC LIMIT 1`);
  const newsRow = (newsLink as any).rows?.[0] ?? null;

  const changed = townMode !== savedRow.town_mode || categoryMode !== savedRow.category_mode;

  return <main className="mx-auto max-w-5xl px-6 py-12">
    <p className="text-sm font-medium uppercase tracking-wide text-brand-600">Protected admin — preview only</p>
    <h1 className="mt-1 text-3xl font-semibold">Logged-out preview</h1>
    <div className="mt-4 rounded-lg border border-blue-300 bg-blue-50 p-4 text-sm text-blue-900">
      <p className="font-semibold">Nothing on this page is saved. This is a read-only simulation.</p>
      <p className="mt-1">Previewing: town mode <strong>{townMode}</strong>, category mode <strong>{categoryMode}</strong>
        {changed ? <> — different from the currently saved <strong>{savedRow.town_mode}</strong> / <strong>{savedRow.category_mode}</strong>.</> : <> — same as the currently saved settings.</>}
      </p>
      <p className="mt-2"><Link href="/directoryadmin/visibility" className="underline">Back to visibility settings</Link></p>
    </div>

    <div className="mt-6 grid gap-4 sm:grid-cols-3">
      <div className="rounded-xl border p-4"><p className="text-2xl font-semibold">{totalsRow.businesses}</p><p className="text-sm text-slate-600">Businesses visible</p></div>
      <div className="rounded-xl border p-4"><p className="text-2xl font-semibold">{totalsRow.towns}</p><p className="text-sm text-slate-600">Towns visible</p></div>
      <div className="rounded-xl border p-4"><p className="text-2xl font-semibold">{totalsRow.categories}</p><p className="text-sm text-slate-600">Categories visible</p></div>
    </div>

    <section className="mt-8 rounded-xl border p-5">
      <h2 className="text-xl font-semibold">Sample of what a visitor would see</h2>
      <ul className="mt-3 divide-y text-sm">
        {((sample as any).rows ?? []).length === 0
          ? <li className="py-2 text-slate-500">No businesses would be publicly visible under this hypothetical scope.</li>
          : ((sample as any).rows as any[]).map((b, i) => <li key={i} className="py-2">{b.business_name} <span className="text-slate-500">— {b.town} · {b.category}</span></li>)}
      </ul>
    </section>

    <section className="mt-6 rounded-xl border p-5">
      <h2 className="text-xl font-semibold">Representative news link</h2>
      {newsRow
        ? <p className="mt-2 text-sm">&ldquo;{newsRow.headline}&rdquo; — {newsRow.town} (<code>/news/{newsRow.slug}</code> would resolve to an eligible town)</p>
        : <p className="mt-2 text-sm text-slate-500">No published story currently falls within a town that would be visible under this hypothetical scope.</p>}
    </section>

    <div className="mt-8 grid gap-8 md:grid-cols-2">
      <section><h2 className="text-xl font-semibold">Towns that would be visible ({((towns as any).rows ?? []).length})</h2>
        <ul className="mt-2 text-sm text-slate-700">{((towns as any).rows ?? []).map((t: any, i: number) => <li key={i}>{t.label} ({t.count})</li>)}</ul>
      </section>
      <section><h2 className="text-xl font-semibold">Categories that would be visible ({((categories as any).rows ?? []).length})</h2>
        <ul className="mt-2 text-sm text-slate-700">{((categories as any).rows ?? []).map((c: any, i: number) => <li key={i}>{c.label} ({c.count})</li>)}</ul>
      </section>
    </div>
  </main>;
}
