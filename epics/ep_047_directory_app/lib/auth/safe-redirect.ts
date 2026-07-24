// Pulled out of login/actions.ts because a "use server" file may only
// export async functions — this is a plain sync helper, and it's also the
// kind of security-relevant logic that deserves a direct unit test rather
// than only being exercised indirectly through a browser login flow.

/**
 * Validates a post-login redirect target. Only same-site paths under
 * /directoryadmin are allowed — rejects protocol-relative ("//evil.com")
 * and absolute ("https://evil.com") targets, which would otherwise make the
 * login form an open redirect.
 */
export function safeNextPath(next: string | null | undefined): string {
  if (!next) return "/directoryadmin/dashboard";
  if (!next.startsWith("/directoryadmin/") || next.startsWith("//") || next.includes("://")) {
    return "/directoryadmin/dashboard";
  }
  return next;
}
