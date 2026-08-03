import Link from "next/link";
import { requireAdminUserForPage } from "@/lib/auth/require";
import { db } from "@/lib/db/client";
import { sql } from "drizzle-orm";
import { saveScope, saveVisibility, saveBusinessOverride, saveNewsDisplaySettings } from "./actions";
import { describeScopeChange } from "@/ep047_visibility_news/lib/scope-diff";

export const dynamic = "force-dynamic";
type VisibilitySearchParams = { q?: string; previewTownMode?: string; previewCategoryMode?: string; scopeApplied?: string };
export default async function VisibilityPage({ searchParams }: { searchParams: Promise<VisibilitySearchParams> }) {
  await requireAdminUserForPage("/directoryadmin/visibility");
  const { q, previewTownMode, previewCategoryMode, scopeApplied } = await searchParams;
  const query = (q ?? "").trim();
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

  const searchResults = query
    ? await db.execute(sql`SELECT b.id, b.business_name, b.town, b.category,
        COALESCE(v.decision, 'inherit') AS decision, v.reason
        FROM businesses b LEFT JOIN public_business_visibility v ON v.business_id = b.id
        WHERE b.business_name ILIKE ${"%" + query + "%"} ORDER BY b.business_name LIMIT 20`)
    : null;
  const currentOverrides = await db.execute(sql`SELECT b.id, b.business_name, b.town, b.category, v.decision, v.reason, v.updated_at
    FROM public_business_visibility v JOIN businesses b ON b.id = v.business_id
    WHERE v.decision <> 'inherit' ORDER BY v.updated_at DESC LIMIT 50`);
  const overrideForm = (biz: any) => <form key={biz.id} action={saveBusinessOverride} className="grid gap-2 border-b py-3 text-sm sm:grid-cols-[1fr,140px,1fr,auto] sm:items-center">
    <input type="hidden" name="businessId" value={biz.id} />
    <input type="hidden" name="returnQuery" value={query} />
    <span><span className="font-medium">{biz.business_name}</span> <span className="text-slate-500">{biz.town} · {biz.category}</span> {biz.decision !== "inherit" && <span className="ml-1 rounded bg-amber-100 px-1.5 py-0.5 text-xs text-amber-800">{biz.decision}</span>}</span>
    <select name="decision" defaultValue={biz.decision} className="rounded border p-1.5"><option value="inherit">Inherit (no override)</option><option value="show">Force show</option><option value="hide">Force hide</option></select>
    <input name="reason" placeholder="Reason (required)" defaultValue={biz.decision !== "inherit" ? biz.reason ?? "" : ""} className="rounded border p-1.5" required />
    <button className="rounded border px-3 py-1.5 text-brand-700">Save override</button>
  </form>;

  // Preview panel: shown only when the scope form was submitted without confirmation
  // (saveScope redirects here with the proposed values instead of writing anything).
  const proposedTownMode = previewTownMode === "selected" ? "selected" : previewTownMode === "all" ? "all" : null;
  const proposedCategoryMode = previewCategoryMode === "selected" ? "selected" : previewCategoryMode === "all" ? "all" : null;
  const scopePreview = proposedTownMode && proposedCategoryMode ? (() => {
    const lines = describeScopeChange({
      currentTownMode: row.town_mode,
      currentCategoryMode: row.category_mode,
      proposedTownMode,
      proposedCategoryMode,
      disabledTownLabels: ((towns as any).rows ?? []).filter((t: any) => !t.enabled).map((t: any) => t.label),
      disabledCategoryLabels: ((categories as any).rows ?? []).filter((c: any) => !c.enabled).map((c: any) => c.label),
    });
    return <div className="mt-4 rounded-lg border border-amber-300 bg-amber-50 p-4 text-sm">
      <p className="font-semibold text-amber-900">Preview — nothing has been saved yet</p>
      <ul className="mt-2 list-disc pl-5 text-amber-900">{lines.map((line, i) => <li key={i}>{line}</li>)}</ul>
      <form action={saveScope} className="mt-3 flex items-center gap-3">
        <input type="hidden" name="townMode" value={proposedTownMode} />
        <input type="hidden" name="categoryMode" value={proposedCategoryMode} />
        <input type="hidden" name="confirmed" value="1" />
        <button className="rounded bg-amber-700 px-4 py-2 text-white">Confirm &amp; apply</button>
        <Link href={`/directoryadmin/visibility/preview?townMode=${proposedTownMode}&categoryMode=${proposedCategoryMode}`} className="text-amber-900 underline">See a logged-out preview first</Link>
        <Link href="/directoryadmin/visibility" className="text-amber-900 underline">Cancel</Link>
      </form>
    </div>;
  })() : null;
  return <main className="mx-auto max-w-5xl px-6 py-12"><p className="text-sm font-medium uppercase tracking-wide text-brand-600">Protected admin</p><h1 className="mt-1 text-3xl font-semibold">Public visibility</h1><p className="mt-2 text-slate-600">Hidden records remain stored and available to administrators.</p>
  {scopeApplied === "1" && !scopePreview && <div className="mt-4 rounded-lg border border-green-300 bg-green-50 p-3 text-sm text-green-900">Scope change applied and recorded in the audit log.</div>}
  <form action={saveScope} className="mt-8 grid gap-4 rounded-xl border p-5 sm:grid-cols-3"><label>Town mode<select name="townMode" defaultValue={row.town_mode} className="mt-1 block rounded border p-2"><option value="all">Show all towns</option><option value="selected">Selected towns only</option></select></label><label>Category mode<select name="categoryMode" defaultValue={row.category_mode} className="mt-1 block rounded border p-2"><option value="all">Show all categories</option><option value="selected">Selected categories only</option></select></label><button className="self-end rounded bg-brand-600 px-4 py-2 text-white">Preview scope change</button></form>
  {scopePreview}
  <form action={saveNewsDisplaySettings} className="mt-5 grid gap-4 rounded-xl border border-brand-200 bg-brand-50 p-5 sm:grid-cols-3"><div><h2 className="font-semibold">News display limits</h2><p className="text-sm text-slate-600">Preview/apply is explicit and older records remain stored.</p></div><label>Max articles per town<input name="maxArticlesPerTown" type="number" min="1" max="100" defaultValue={displayRow.max_articles_per_town} className="mt-1 block rounded border p-2" /></label><label>Lookback days<input name="lookbackDays" type="number" min="1" max="3650" defaultValue={displayRow.lookback_days} className="mt-1 block rounded border p-2" /></label><button className="rounded bg-brand-600 px-4 py-2 text-white sm:col-start-3">Apply News limits (explicit)</button></form><div className="mt-8 grid gap-8 md:grid-cols-2"><section><h2 className="text-xl font-semibold">Towns / locations</h2>{render("town", (towns as any).rows ?? [])}</section><section><h2 className="text-xl font-semibold">Categories</h2>{render("category", (categories as any).rows ?? [])}</section></div>
    <section className="mt-10 rounded-xl border p-5">
      <h2 className="text-xl font-semibold">Business-level override</h2>
      <p className="mt-1 text-sm text-slate-600">Handle one named listing as an exception without changing the whole town or category. A reason is required and every change is audited.</p>
      <form method="get" className="mt-4 flex gap-2"><input name="q" defaultValue={query} placeholder="Search business name" className="flex-1 rounded border p-2" /><button className="rounded border px-4 py-2">Search</button></form>
      {query && <div className="mt-3">{((searchResults as any)?.rows ?? []).length === 0 ? <p className="text-sm text-slate-500">No businesses match &ldquo;{query}&rdquo;.</p> : ((searchResults as any).rows as any[]).map(overrideForm)}</div>}
      <h3 className="mt-6 text-sm font-semibold uppercase tracking-wide text-slate-500">Active overrides</h3>
      <div className="mt-2">{((currentOverrides as any).rows ?? []).length === 0 ? <p className="text-sm text-slate-500">No business currently has an override.</p> : ((currentOverrides as any).rows as any[]).map(overrideForm)}</div>
    </section>
  </main>;
}
