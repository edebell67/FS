import Link from "next/link";

/**
 * No auth/roles exist yet — that part of Phase 4 (Auth.js + the six roles)
 * hasn't been built. These admin links are plain nav items for now; once
 * roles land, they move behind a role check rather than being removed from
 * here.
 */
export function SiteHeader() {
  return (
    <header className="border-b border-slate-200">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <Link href="/directory" className="text-lg font-semibold tracking-tight text-slate-900">
          The Directory
        </Link>
        <nav className="flex items-center gap-6 text-sm font-medium text-slate-600">
          <Link href="/directory/search" className="hover:text-slate-900">
            Search
          </Link>
          <span className="h-4 w-px bg-slate-200" aria-hidden="true" />
          <Link href="/directoryadmin/dashboard" className="hover:text-slate-900">
            Dashboard
          </Link>
          <Link href="/directoryadmin/pipeline" className="hover:text-slate-900">
            Pipeline
          </Link>
          <Link href="/directoryadmin/businesses" className="hover:text-slate-900">
            Businesses
          </Link>
          <Link
            href="/directoryadmin/import"
            className="rounded-md bg-brand-600 px-3 py-1.5 text-white hover:bg-brand-700"
          >
            Import
          </Link>
        </nav>
      </div>
    </header>
  );
}
