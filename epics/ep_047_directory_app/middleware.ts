// Edge-runtime pre-filter for /directoryadmin/*. This is NOT the
// authoritative auth check — Edge middleware can't run `pg` or
// `node:crypto`'s scrypt, so it can only check whether a session cookie is
// present, not whether it's actually valid/unexpired. That real check
// happens in lib/auth/require.ts, called by every protected page and API
// route (Node.js runtime). See lib/auth/session.ts's header comment for the
// full two-layer rationale — this file is the fast/cheap layer only.
//
// Concretely: a forged or stale cookie value gets past THIS filter but is
// rejected by the DB-backed check downstream. A missing cookie is rejected
// right here, which covers the overwhelming majority of unauthenticated
// requests without a database round-trip.

import { NextResponse, type NextRequest } from "next/server";
import { SESSION_COOKIE_NAME } from "@/lib/auth/cookie-name";

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // The login page and its own API must stay reachable, or nobody could
  // ever log in.
  if (pathname === "/directoryadmin/login" || pathname === "/directoryadmin/api/login") {
    return NextResponse.next();
  }

  const hasSessionCookie = Boolean(request.cookies.get(SESSION_COOKIE_NAME)?.value);
  if (hasSessionCookie) {
    return NextResponse.next();
  }

  if (pathname.startsWith("/directoryadmin/api/")) {
    return NextResponse.json({ error: "Not authenticated." }, { status: 401 });
  }

  const loginUrl = new URL("/directoryadmin/login", request.url);
  loginUrl.searchParams.set("next", pathname);
  return NextResponse.redirect(loginUrl);
}

export const config = {
  matcher: ["/directoryadmin/:path*"],
};
