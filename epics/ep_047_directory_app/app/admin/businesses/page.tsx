import Link from "next/link";
import { format } from "date-fns";
import {
  listBusinesses,
  listDistinctCategories,
  listDistinctTowns,
  parsePage,
  PAGE_SIZE,
} from "@/lib/db/queries/businesses";

export const dynamic = "force-dynamic";

interface PageProps {
  searchParams: Promise<{
    q?: string;
    category?: string;
    town?: string;
    status?: string;
    stage?: string;
    column?: string;
    page?: string;
  }>;
}

function buildQueryString(
  params: Record<string, string | undefined>,
  overrides: Record<string, string | number | undefined>
): string {
  const merged = new URLSearchParams();
  for (const [key, value] of Object.entries({ ...params, ...overrides })) {
    if (value !== undefined && value !== "") merged.set(key, String(value));
  }
  const qs = merged.toString();
  return qs ? `?${qs}` : "";
}

export default async function BusinessesPage({ searchParams }: PageProps) {
  const params = await searchParams;
  const page = parsePage(params.page);

  const [{ rows, total, pageCount }, categories, towns] = await Promise.all([
    listBusinesses({
      q: params.q,
      category: params.category,
      town: params.town,
      status: params.status,
      stageKey: params.stage,
      boardColumn: params.column,
      page,
    }),
    listDistinctCategories(),
    listDistinctTowns(),
  ]);

  const hasFilters = Boolean(
    params.q || params.category || params.town || params.status || params.stage || params.column
  );

  return (
    <main className="mx-auto max-w-6xl px-6 py-12">
      <p className="text-sm font-medium uppercase tracking-wide text-brand-600">Admin — Businesses</p>
      <div className="mt-1 flex items-baseline justify-between">
        <h1 className="text-2xl font-semibold tracking-tight text-slate-900">Businesses</h1>
        <Link href="/admin/import" className="text-sm font-medium text-brand-600 hover:text-brand-700">
          Import more →
        </Link>
      </div>
      <p className="mt-2 text-slate-600">
        {total} business{total === 1 ? "" : "es"}
        {hasFilters ? " matching your filters" : " in the directory"}.
        {params.stage && (
          <>
            {" "}
            Filtered to stage <span className="font-medium">{params.stage}</span> —{" "}
            <Link href="/admin/businesses" className="text-brand-600 hover:underline">
              clear
            </Link>
            .
          </>
        )}
        {params.column && (
          <>
            {" "}
            Filtered to board column <span className="font-medium">{params.column}</span> —{" "}
            <Link href="/admin/businesses" className="text-brand-600 hover:underline">
              clear
            </Link>
            .
          </>
        )}
      </p>

      <form className="mt-6 grid grid-cols-1 gap-3 sm:grid-cols-4" action="/admin/businesses">
        <input
          type="text"
          name="q"
          defaultValue={params.q ?? ""}
          placeholder="Search name, category, town, email, phone, ref, postcode…"
          className="rounded-md border border-slate-300 px-3 py-2 text-sm sm:col-span-2"
        />
        <select
          name="category"
          defaultValue={params.category ?? ""}
          className="rounded-md border border-slate-300 px-3 py-2 text-sm capitalize"
        >
          <option value="">All categories</option>
          {categories.map((c) => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </select>
        <select
          name="town"
          defaultValue={params.town ?? ""}
          className="rounded-md border border-slate-300 px-3 py-2 text-sm capitalize"
        >
          <option value="">All towns</option>
          {towns.map((t) => (
            <option key={t} value={t}>
              {t}
            </option>
          ))}
        </select>
        <div className="sm:col-span-4 flex items-center gap-3">
          <button
            type="submit"
            className="rounded-md bg-brand-600 px-4 py-2 text-sm font-medium text-white hover:bg-brand-700"
          >
            Filter
          </button>
          {hasFilters && (
            <Link href="/admin/businesses" className="text-sm font-medium text-slate-500 hover:text-slate-700">
              Clear filters
            </Link>
          )}
        </div>
      </form>

      <div className="mt-6 overflow-x-auto rounded-xl border border-slate-200">
        <table className="w-full text-left text-sm">
          <thead className="bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
            <tr>
              <th className="px-4 py-2 font-medium">Ref</th>
              <th className="px-4 py-2 font-medium">Name</th>
              <th className="px-4 py-2 font-medium">Category</th>
              <th className="px-4 py-2 font-medium">Town</th>
              <th className="px-4 py-2 font-medium">Phone</th>
              <th className="px-4 py-2 font-medium">Email</th>
              <th className="px-4 py-2 font-medium">Stage</th>
              <th className="px-4 py-2 font-medium">Imported</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {rows.length === 0 ? (
              <tr>
                <td colSpan={8} className="px-4 py-8 text-center text-slate-500">
                  No businesses match these filters.
                </td>
              </tr>
            ) : (
              rows.map((row) => (
                <tr key={row.id}>
                  <td className="whitespace-nowrap px-4 py-2 font-mono text-xs text-slate-500">
                    {row.businessRef}
                  </td>
                  <td className="whitespace-nowrap px-4 py-2 font-medium text-slate-900">
                    <Link href={`/admin/businesses/${row.businessRef}`} className="hover:text-brand-600 hover:underline">
                      {row.businessName}
                    </Link>
                  </td>
                  <td className="whitespace-nowrap px-4 py-2 capitalize text-slate-600">{row.category}</td>
                  <td className="whitespace-nowrap px-4 py-2 capitalize text-slate-600">{row.town ?? "—"}</td>
                  <td className="whitespace-nowrap px-4 py-2 text-slate-600">{row.phone ?? "—"}</td>
                  <td className="max-w-[14rem] truncate px-4 py-2 text-slate-600">{row.email ?? "—"}</td>
                  <td className="whitespace-nowrap px-4 py-2">
                    <span className="rounded-full bg-blue-50 px-2 py-0.5 text-xs font-medium text-blue-700">
                      {row.stageLabel ?? "—"}
                    </span>
                  </td>
                  <td className="whitespace-nowrap px-4 py-2 text-slate-500">
                    {format(row.importDate, "d MMM yyyy")}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {pageCount > 1 && (
        <div className="mt-4 flex items-center justify-between text-sm text-slate-600">
          <span>
            Page {page} of {pageCount} ({PAGE_SIZE} per page)
          </span>
          <div className="flex gap-2">
            {page > 1 && (
              <Link
                href={`/admin/businesses${buildQueryString(params, { page: page - 1 })}`}
                className="rounded-md border border-slate-300 px-3 py-1.5 font-medium hover:bg-slate-50"
              >
                ← Previous
              </Link>
            )}
            {page < pageCount && (
              <Link
                href={`/admin/businesses${buildQueryString(params, { page: page + 1 })}`}
                className="rounded-md border border-slate-300 px-3 py-1.5 font-medium hover:bg-slate-50"
              >
                Next →
              </Link>
            )}
          </div>
        </div>
      )}
    </main>
  );
}
