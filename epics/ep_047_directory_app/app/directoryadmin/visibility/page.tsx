import { requireAdminUserForPage } from "@/lib/auth/require";
import { db } from "@/lib/db/client";
import { sql } from "drizzle-orm";
import { saveScope, saveVisibility, saveNewsDisplaySettings } from "./actions";

export const dynamic = "force-dynamic";
export default async function VisibilityPage() {
  await requireAdminUserForPage("/directoryadmin/visibility");
  const settings = await db.execute(sql`SELECT town_mode, category_mode FROM public_directory_settings WHERE id='default'`);
  const row = (settings as any).rows?.[0] ?? { town_mode: "all", category_mode: "all" };
  const displaySettings = await db.execute(sql`SELECT max_articles_per_town, lookback_days FROM public_news_display_settings WHERE id=true`);
  const displayRow = (displaySettings as any).rows?.[0] ?? { max_articles_per_town: 10, lookback_days: 30 };
  const towns = await db.execute(sql`SELECT initcap(trim(b.town)) AS label, lower(trim(b.town)) AS key,
    COALESCE(bool_or(t.is_enabled), true) AS enabled, count(*)::int AS count
    FROM businesses b LEFT JOIN public_town_visibility t ON t.town_key=lower(trim(b.town))
    WHERE b.town IS NOT NULL AND trim(b.town) <> ''
    GROUP BY initcap(trim(b.town)), lower(trim(b.town)) ORDER BY label`);
  const categories = await db.execute(sql`SELECT initcap(trim(b.category)) AS label, lower(trim(b.category)) AS key,
    COALESCE(bool_or(c.is_enabled), true) AS enabled, count(*)::int AS count
    FROM businesses b LEFT JOIN public_category_visibility c ON c.category_key=lower(trim(b.category))
    WHERE b.category IS NOT NULL AND trim(b.category) <> ''
    GROUP BY initcap(trim(b.category)), lower(trim(b.category)) ORDER BY label`);
  const render = (kind: string, items: any[]) => items.map((item) => <form key={item.key} action={saveVisibility} className="flex items-center gap-3 border-b py-2 text-sm"><input type="hidden" name="kind" value={kind}/><input type="hidden" name="key" value={item.key}/><input type="hidden" name="label" value={item.label}/><input type="checkbox" name="enabled" defaultChecked={item.enabled}/><span className="flex-1">{item.label} <span className="text-slate-500">({item.count})</span></span><button className="text-brand-700">Save</button></form>);
  return <main className="mx-auto max-w-5xl px-6 py-12"><p className="text-sm font-medium uppercase tracking-wide text-brand-600">Protected admin</p><h1 className="mt-1 text-3xl font-semibold">Public visibility</h1><p className="mt-2 text-slate-600">Hidden records remain stored and available to administrators.</p><form action={saveScope} className="mt-8 grid gap-4 rounded-xl border p-5 sm:grid-cols-3"><label>Town mode<select name="townMode" defaultValue={row.town_mode} className="mt-1 block rounded border p-2"><option value="all">Show all towns</option><option value="selected">Selected towns only</option></select></label><label>Category mode<select name="categoryMode" defaultValue={row.category_mode} className="mt-1 block rounded border p-2"><option value="all">Show all categories</option><option value="selected">Selected categories only</option></select></label><button className="self-end rounded bg-brand-600 px-4 py-2 text-white">Save scope (explicit)</button></form><form action={saveNewsDisplaySettings} className="mt-5 grid gap-4 rounded-xl border border-brand-200 bg-brand-50 p-5 sm:grid-cols-3"><div><h2 className="font-semibold">News display limits</h2><p className="text-sm text-slate-600">Preview/apply is explicit and older records remain stored.</p></div><label>Max articles per town<input name="maxArticlesPerTown" type="number" min="1" max="100" defaultValue={displayRow.max_articles_per_town} className="mt-1 block rounded border p-2" /></label><label>Lookback days<input name="lookbackDays" type="number" min="1" max="3650" defaultValue={displayRow.lookback_days} className="mt-1 block rounded border p-2" /></label><button className="rounded bg-brand-600 px-4 py-2 text-white sm:col-start-3">Apply News limits (explicit)</button></form><div className="mt-8 grid gap-8 md:grid-cols-2"><section><h2 className="text-xl font-semibold">Towns / locations</h2>{render("town", (towns as any).rows ?? [])}</section><section><h2 className="text-xl font-semibold">Categories</h2>{render("category", (categories as any).rows ?? [])}</section></div></main>;
}
