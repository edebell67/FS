import { requireAdminUserForPage } from "@/lib/auth/require";
import { db } from "@/lib/db/client";
import { sql } from "drizzle-orm";
import { saveScope, saveVisibility } from "./actions";

export const dynamic = "force-dynamic";
export default async function VisibilityPage() {
  await requireAdminUserForPage("/directoryadmin/visibility");
  const settings = await db.execute(sql`SELECT town_mode, category_mode FROM public_directory_settings WHERE id='default'`);
  const row = (settings as any).rows?.[0] ?? { town_mode: "all", category_mode: "all" };
  const towns = await db.execute(sql`SELECT town_label AS label, town_key AS key, is_enabled AS enabled, count(b.id)::int AS count
    FROM public_town_visibility t LEFT JOIN businesses b ON lower(trim(b.town))=t.town_key GROUP BY t.town_label,t.town_key,t.is_enabled ORDER BY t.town_label`);
  const categories = await db.execute(sql`SELECT category_label AS label, category_key AS key, is_enabled AS enabled, count(b.id)::int AS count
    FROM public_category_visibility c LEFT JOIN businesses b ON lower(trim(b.category))=c.category_key GROUP BY c.category_label,c.category_key,c.is_enabled ORDER BY c.category_label`);
  const render = (kind: string, items: any[]) => items.map((item) => <form key={item.key} action={saveVisibility} className="flex items-center gap-3 border-b py-2 text-sm"><input type="hidden" name="kind" value={kind}/><input type="hidden" name="key" value={item.key}/><input type="hidden" name="label" value={item.label}/><input type="checkbox" name="enabled" defaultChecked={item.enabled}/><span className="flex-1">{item.label} <span className="text-slate-500">({item.count})</span></span><button className="text-brand-700">Save</button></form>);
  return <main className="mx-auto max-w-5xl px-6 py-12"><p className="text-sm font-medium uppercase tracking-wide text-brand-600">Protected admin</p><h1 className="mt-1 text-3xl font-semibold">Public visibility</h1><p className="mt-2 text-slate-600">Hidden records remain stored and available to administrators.</p><form action={saveScope} className="mt-8 grid gap-4 rounded-xl border p-5 sm:grid-cols-3"><label>Town mode<select name="townMode" defaultValue={row.town_mode} className="mt-1 block rounded border p-2"><option value="all">Show all towns</option><option value="selected">Selected towns only</option></select></label><label>Category mode<select name="categoryMode" defaultValue={row.category_mode} className="mt-1 block rounded border p-2"><option value="all">Show all categories</option><option value="selected">Selected categories only</option></select></label><button className="self-end rounded bg-brand-600 px-4 py-2 text-white">Save scope (explicit)</button></form><div className="mt-8 grid gap-8 md:grid-cols-2"><section><h2 className="text-xl font-semibold">Towns / locations</h2>{render("town", (towns as any).rows ?? [])}</section><section><h2 className="text-xl font-semibold">Categories</h2>{render("category", (categories as any).rows ?? [])}</section></div></main>;
}
