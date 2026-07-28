import Link from "next/link";
import { getCurrentUser } from "@/lib/auth/session";
import { logoutAction } from "@/app/directoryadmin/login/actions";

/**
 * Rendered on every page (root layout), including the fully public
 * /directory/* pages — getCurrentUser() returns null immediately when
 * there's no session cookie, before touching the database, so logged-out
 * visitors (the overwhelming majority of traffic) pay no DB cost here.
 *
 * Roles aren't enforced yet (see AUTH_PLAN.md §4) — any authenticated user
 * sees the full admin nav regardless of role.
 */
export async function SiteHeader() {
  const user = await getCurrentUser();

  return (
    <header className="border-b border-[#152022] bg-[#f6f3ed]">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <Link href="/directory" className="font-display text-2xl font-semibold tracking-[-0.04em] text-[#152022]">
          The <span className="text-brand-600">Directory</span>
        </Link>
        <nav className="flex items-center gap-6 text-sm font-medium text-[#4c5657]">
          <Link href="/directory/search" className="hover:text-brand-700">
            Search
          </Link>
          <a href="https://thetechprinciple.com/news/" className="hover:text-brand-700">
            News
          </a>
          {user ? (
            <>
              <span className="h-4 w-px bg-[#d6d2c9]" aria-hidden="true" />
              <Link href="/directoryadmin/dashboard" className="hover:text-slate-900">
                Dashboard
              </Link>
              <Link href="/directoryadmin/pipeline" className="hover:text-slate-900">
                Pipeline
              </Link>
              <Link href="/directoryadmin/businesses" className="hover:text-slate-900">
                Businesses
              </Link>
              {["super_admin", "admin", "operations"].includes(user.role) && <Link href="/directoryadmin/claims" className="hover:text-slate-900">
                Claims
              </Link>}
              {["super_admin", "admin", "operations"].includes(user.role) && <Link href="/directoryadmin/validation" className="hover:text-slate-900">
                Validation
              </Link>}
              <Link
                href="/directoryadmin/import"
                className="rounded-sm bg-brand-600 px-3 py-1.5 text-white hover:bg-brand-700"
              >
                Import
              </Link>
              <span className="h-4 w-px bg-slate-200" aria-hidden="true" />
              <span className="text-[#7a8587]">{user.email}</span>
              <form action={logoutAction}>
                <button type="submit" className="hover:text-slate-900">
                  Sign out
                </button>
              </form>
            </>
          ) : (
            <>
              <span className="h-4 w-px bg-[#d6d2c9]" aria-hidden="true" />
              <Link href="/directoryadmin/login" className="hover:text-slate-900">
                Admin sign in
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}
