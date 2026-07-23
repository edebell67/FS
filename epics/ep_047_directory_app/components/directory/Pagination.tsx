import Link from "next/link";

export interface PaginationProps {
  page: number;
  pageCount: number;
  /** Base path plus any filters to preserve, e.g. "/category/plumbing?sort=name". Page gets appended/merged. */
  basePath: string;
  searchParams?: Record<string, string | undefined>;
}

function hrefFor(basePath: string, searchParams: Record<string, string | undefined> | undefined, page: number) {
  const params = new URLSearchParams();
  for (const [key, value] of Object.entries(searchParams ?? {})) {
    if (value) params.set(key, value);
  }
  params.set("page", String(page));
  return `${basePath}?${params.toString()}`;
}

export function Pagination({ page, pageCount, basePath, searchParams }: PaginationProps) {
  if (pageCount <= 1) return null;

  return (
    <div className="mt-6 flex items-center justify-between text-sm text-slate-600">
      <span>
        Page {page} of {pageCount}
      </span>
      <div className="flex gap-2">
        {page > 1 && (
          <Link
            href={hrefFor(basePath, searchParams, page - 1)}
            className="rounded-md border border-slate-300 px-3 py-1.5 font-medium hover:bg-slate-50"
          >
            ← Previous
          </Link>
        )}
        {page < pageCount && (
          <Link
            href={hrefFor(basePath, searchParams, page + 1)}
            className="rounded-md border border-slate-300 px-3 py-1.5 font-medium hover:bg-slate-50"
          >
            Next →
          </Link>
        )}
      </div>
    </div>
  );
}
