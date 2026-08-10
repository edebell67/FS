import Link from "next/link";
import { getCurrentUser } from "@/lib/auth/session";
import { logoutAction } from "@/app/directoryadmin/login/actions";
import { AdminMenuModal } from "@/components/admin/AdminMenuModal";
import { SiteHeaderNav } from "@/components/layout/SiteHeaderNav";

/**
 * Rendered on every page (root layout), including the fully public
 * /directory/* pages — getCurrentUser() returns null immediately when
 * there's no session cookie, before touching the database, so logged-out
 * visitors (the overwhelming majority of traffic) pay no DB cost here.
 *
 * Roles aren't enforced yet (see AUTH_PLAN.md §4) — any authenticated user
 * sees the full admin nav regardless of role.
 *
 * On verify/claim pages, navigation links are disabled to keep business
 * owners focused on completing their form.
 */
export async function SiteHeader() {
  const user = await getCurrentUser();

  return (
    <header className="border-b border-[#152022] bg-[#f6f3ed]">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <div className="font-display text-2xl font-semibold tracking-[-0.04em] text-[#152022]">
          TTP <span className="text-brand-600">Directory</span>
        </div>
        <div className="flex items-center gap-6 text-sm font-medium text-[#4c5657]">
          <SiteHeaderNav />
          {user ? (
            <>
              <span className="h-4 w-px bg-[#d6d2c9]" aria-hidden="true" />
              <AdminMenuModal role={user.role} />
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
        </div>
      </div>
    </header>
  );
}
