// Thin wrappers around getCurrentUser() for the two call sites that need
// different failure behavior: a page redirects to login, an API route
// returns 401 JSON. Middleware (Edge, cookie-presence only) is the first,
// cheap filter — these are the authoritative check, see session.ts's header
// comment for the full two-layer rationale.

import { redirect } from "next/navigation";
import { NextResponse } from "next/server";
import { getCurrentUser, type CurrentUser } from "./session";

/** Call at the top of every protected Server Component page. Redirects if not logged in. */
export async function requireAdminUserForPage(currentPath: string): Promise<CurrentUser> {
  const user = await getCurrentUser();
  if (!user) {
    redirect(`/directoryadmin/login?next=${encodeURIComponent(currentPath)}`);
  }
  return user;
}

/**
 * Call at the top of every protected Route Handler. Returns the user, or a
 * 401 NextResponse the caller must return immediately:
 *   const auth = await requireAdminUserForApi();
 *   if (auth instanceof NextResponse) return auth;
 */
export async function requireAdminUserForApi(): Promise<CurrentUser | NextResponse> {
  const user = await getCurrentUser();
  if (!user) {
    return NextResponse.json({ error: "Not authenticated." }, { status: 401 });
  }
  return user;
}
