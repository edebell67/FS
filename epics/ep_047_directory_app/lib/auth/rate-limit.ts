// In-memory login rate limiting, keyed by email. Deliberately not
// database-backed: it resets on every deploy and doesn't span multiple
// instances, which is an acceptable tradeoff for a single starter Render
// instance (see AUTH_PLAN's Risks/Notes). Move this to the DB or Redis if
// this ever scales out to multiple instances.

const MAX_ATTEMPTS = 5;
const WINDOW_MS = 15 * 60 * 1000; // 15 minutes

interface Attempt {
  count: number;
  windowStart: number;
}

const attempts = new Map<string, Attempt>();

/** Returns true if this email is currently rate-limited (too many recent failures). */
export function isRateLimited(email: string): boolean {
  const entry = attempts.get(email.toLowerCase());
  if (!entry) return false;
  if (Date.now() - entry.windowStart > WINDOW_MS) {
    attempts.delete(email.toLowerCase());
    return false;
  }
  return entry.count >= MAX_ATTEMPTS;
}

/** Record a failed login attempt for this email. */
export function recordFailedAttempt(email: string): void {
  const key = email.toLowerCase();
  const entry = attempts.get(key);
  if (!entry || Date.now() - entry.windowStart > WINDOW_MS) {
    attempts.set(key, { count: 1, windowStart: Date.now() });
  } else {
    entry.count += 1;
  }
}

/** Clear failed-attempt tracking for this email — call on successful login. */
export function clearFailedAttempts(email: string): void {
  attempts.delete(email.toLowerCase());
}
