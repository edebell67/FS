import type { Metadata } from "next";
import Link from "next/link";
import { listBusinesses, listDistinctCategories, listDistinctTowns, parsePage } from "@/lib/db/queries/businesses";
import { BusinessCard } from "@/components/directory/BusinessCard";
import { Pagination } from "@/components/directory/Pagination";

export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title: "Search",
  description: "Search the business directory by name, category, or town.",
};

interface PageProps {
  searchParams: Promise<{
    q?: string;
    category?: string;
    town?: string;
    letter?: string;
    page?: string;
  }>;
}

export default async function SearchPage({ searchParams }: PageProps) {
  const params = await searchParams;
  const page = parsePage(params.page);

  const [{ rows, total, pageCount }, categories, towns] = await Promise.all([
    listBusinesses({
      q: params.q,
      category: params.category,
      town: params.town,
      startsWith: params.letter,
      page,
      sort: "name",
    }),
    listDistinctCategories(),
    listDistinctTowns(),
  ]);

  const hasFilters = Boolean(params.q || params.category || params.town || params.letter);

  return (
    <main className="mx-auto max-w-4xl px-6 py-12">
      <h1 className="text-2xl font-semibold tracking-tight text-slate-900">Search</h1>
      <p className="mt-2 text-slate-600">
        {total} business{total === 1 ? "" : "es"}
        {hasFilters ? " match your search." : " in the directory."}
      </p>

      <form className="mt-6 grid grid-cols-1 gap-3 sm:grid-cols-4" action="/directory/search">
        <input
          type="text"
          name="q"
          defaultValue={params.q ?? ""}
          placeholder="Search name, town, category…"
          className="rounded-md border border-slate-300 px-3 py-2 text-sm sm:col-span-2"
        />
        <select name="category" defaultValue={params.category ?? ""} className="rounded-md border border-slate-300 px-3 py-2 text-sm capitalize">
          <option value="">All categories</option>
          {categories.map((c) => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </select>
        <select name="town" defaultValue={params.town ?? ""} className="rounded-md border border-slate-300 px-3 py-2 text-sm capitalize">
          <option value="">All towns</option>
          {towns.map((t) => (
            <option key={t} value={t}>
              {t}
            </option>
          ))}
        </select>
        <div className="sm:col-span-4 flex items-center gap-3">
          <button type="submit" className="rounded-md bg-brand-600 px-4 py-2 text-sm font-medium text-white hover:bg-brand-700">
            Search
          </button>
          {hasFilters && (
            <Link href="/directory/search" className="text-sm font-medium text-slate-500 hover:text-slate-700">
              Clear filters
            </Link>
          )}
          {params.letter && (
            <span className="text-sm text-slate-500">
              Showing names starting with <span className="font-medium">{params.letter}</span>
            </span>
          )}
        </div>
      </form>

      <div className="mt-8 grid grid-cols-1 gap-3 sm:grid-cols-2">
        {rows.length === 0 ? (
          <p className="col-span-full rounded-lg bg-slate-50 px-4 py-8 text-center text-slate-500">
            No businesses match these filters.
          </p>
        ) : (
          rows.map((row) => <BusinessCard key={row.id} business={row} />)
        )}
      </div>

      <Pagination
        page={page}
        pageCount={pageCount}
        basePath="/directory/search"
        searchParams={{ q: params.q, category: params.category, town: params.town, letter: params.letter }}
      />
    </main>
  );
}
