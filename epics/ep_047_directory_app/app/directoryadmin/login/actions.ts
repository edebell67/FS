"use server";

import { redirect } from "next/navigation";
import { eq } from "drizzle-orm";
import { db } from "@/lib/db/client";
import { users } from "@/lib/db/schema";
import { verifyPassword } from "@/lib/auth/password";
import { createSession, destroySession } from "@/lib/auth/session";
import { isRateLimited, recordFailedAttempt, clearFailedAttempts } from "@/lib/auth/rate-limit";
import { safeNextPath } from "@/lib/auth/safe-redirect";

// A precomputed hash of a password nobody will ever type. Verifying against
// this for unknown emails means a login attempt costs the same scrypt work
// whether the email exists or not — response timing can't be used to
// enumerate which emails have accounts.
const DUMMY_HASH =
  "scrypt$s2JJQNc1ZVfR-SWIOjB7Gw$02JT7U3UWKWJcywoenZ_xSa8B2GKrTmR5_ye72hb94ZawR008zNYegDqONzcxLYyys4iJE5-FgM5-6K_I-w26g";

export async function loginAction(formData: FormData): Promise<void> {
  const email = String(formData.get("email") ?? "").trim();
  const password = String(formData.get("password") ?? "");
  const next = safeNextPath(formData.get("next") ? String(formData.get("next")) : null);

  if (!email || !password) {
    redirect(`/directoryadmin/login?error=1&next=${encodeURIComponent(next)}`);
  }

  if (isRateLimited(email)) {
    redirect(`/directoryadmin/login?error=rate_limited&next=${encodeURIComponent(next)}`);
  }

  const [user] = await db.select().from(users).where(eq(users.email, email)).limit(1);

  // Always verify — against the real hash if the user exists, against the
  // dummy hash if not — so this branch takes the same time either way.
  const valid = await verifyPassword(password, user?.passwordHash ?? DUMMY_HASH);

  if (!user || !valid) {
    recordFailedAttempt(email);
    redirect(`/directoryadmin/login?error=1&next=${encodeURIComponent(next)}`);
  }

  clearFailedAttempts(email);
  await createSession(user.id);
  await db.update(users).set({ lastLoginAt: new Date() }).where(eq(users.id, user.id));

  redirect(next);
}

export async function logoutAction(): Promise<void> {
  await destroySession();
  redirect("/directoryadmin/login");
}
