// Session management for the admin console. Two-layer design, deliberately:
//
//   1. middleware.ts (Edge runtime) does a CHEAP check — is there a session
//      cookie at all? — and redirects/401s immediately if not. Edge runtime
//      can't run `pg` or `node:crypto`'s scrypt, so it cannot validate the
//      session against the database.
//   2. Every protected page and API route calls requireAdminUserForPage/Api
//      (lib/auth/require.ts), which calls getCurrentUser() below — Node.js
//      runtime, does the REAL check: hash the cookie, look it up in
//      `sessions`, confirm it hasn't expired. This is the layer that
//      actually decides "is this request authenticated" — middleware is a
//      fast pre-filter, not the source of truth.
//
// SESSION_COOKIE_NAME is re-exported from ./cookie-name (not defined here)
// so middleware.ts can import just the constant without pulling this
// module's `db`/`node:crypto` imports into the Edge bundle.
//
// Tokens are 256 bits of CSPRNG randomness. Only the SHA-256 hash of the
// token is ever written to the database — a database leak alone does not
// hand out usable sessions, since the raw token can't be recovered from the
// hash. AUTH_SECRET is NOT used anywhere in this file: sessions are opaque
// lookup keys, not signed/encoded tokens, so there is nothing to sign.

import { randomBytes, createHash } from "node:crypto";
import { cookies } from "next/headers";
import { eq, lt } from "drizzle-orm";
import { db } from "@/lib/db/client";
import { sessions, users } from "@/lib/db/schema";
import { SESSION_COOKIE_NAME } from "./cookie-name";

export { SESSION_COOKIE_NAME };
const SESSION_TTL_MS = 7 * 24 * 60 * 60 * 1000; // 7 days
// Renew (push expiry back out to the full TTL) once a session is within this
// much of expiring, so an active user doesn't get logged out mid-task.
const RENEW_THRESHOLD_MS = 24 * 60 * 60 * 1000; // 1 day

export interface CurrentUser {
  id: string;
  email: string;
  role: string;
}

function hashToken(token: string): string {
  return createHash("sha256").update(token).digest("hex");
}

/**
 * Creates a new session row and sets the cookie. Must be called from a
 * Server Action or Route Handler (Next.js only allows setting cookies from
 * those contexts, not from a Server Component render).
 */
export async function createSession(userId: string): Promise<void> {
  const token = randomBytes(32).toString("base64url");
  const expiresAt = new Date(Date.now() + SESSION_TTL_MS);

  await db.insert(sessions).values({ userId, tokenHash: hashToken(token), expiresAt });

  const store = await cookies();
  store.set(SESSION_COOKIE_NAME, token, {
    httpOnly: true,
    sameSite: "lax",
    secure: process.env.NODE_ENV === "production",
    path: "/",
    expires: expiresAt,
  });
}

/**
 * The authoritative check. Returns the current user if the cookie names a
 * valid, unexpired session; otherwise null. Safe to call from Server
 * Components (read-only — the DB UPDATE for sliding renewal doesn't require
 * a cookie write, so it's not subject to the "can't set cookies here" rule).
 */
export async function getCurrentUser(): Promise<CurrentUser | null> {
  const store = await cookies();
  const token = store.get(SESSION_COOKIE_NAME)?.value;
  if (!token) return null;

  const tokenHash = hashToken(token);
  const [row] = await db
    .select({
      sessionId: sessions.id,
      expiresAt: sessions.expiresAt,
      userId: users.id,
      email: users.email,
      role: users.role,
    })
    .from(sessions)
    .innerJoin(users, eq(sessions.userId, users.id))
    .where(eq(sessions.tokenHash, tokenHash))
    .limit(1);

  if (!row) return null;
  if (row.expiresAt.getTime() <= Date.now()) {
    // Expired — clean it up opportunistically, no cron needed at this scale.
    await db.delete(sessions).where(eq(sessions.id, row.sessionId));
    return null;
  }

  if (row.expiresAt.getTime() - Date.now() < RENEW_THRESHOLD_MS) {
    await db
      .update(sessions)
      .set({ expiresAt: new Date(Date.now() + SESSION_TTL_MS) })
      .where(eq(sessions.id, row.sessionId));
  }

  return { id: row.userId, email: row.email, role: row.role };
}

/** Deletes the session row and clears the cookie. Server Action/Route Handler only. */
export async function destroySession(): Promise<void> {
  const store = await cookies();
  const token = store.get(SESSION_COOKIE_NAME)?.value;
  if (token) {
    await db.delete(sessions).where(eq(sessions.tokenHash, hashToken(token)));
  }
  store.delete(SESSION_COOKIE_NAME);
}

/** Opportunistic cleanup of expired sessions — call occasionally, no cron required at this scale. */
export async function purgeExpiredSessions(): Promise<number> {
  const deleted = await db.delete(sessions).where(lt(sessions.expiresAt, new Date())).returning({ id: sessions.id });
  return deleted.length;
}
