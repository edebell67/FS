// Generated business sites live in the separate github.com/edebell67/epics
// repo (flat, top-level <slug>/ folders), not the FS monorepo this app
// itself lives in -- confirmed 2026-07-31 against the working example
// dg-maintenance-uk-ltd/. That repo's GitHub Pages previously had a CNAME
// pointing at thetechprinciple.com; once DNS for that domain moved to
// Render, the CNAME had to be removed so the raw github.io URL below
// serves content directly instead of 301-redirecting to the dead domain.
const DEFAULT_GITHUB_PAGES_ORIGIN = "https://edebell67.github.io/epics";

function githubPagesOrigin(): string {
  return (process.env.GITHUB_PAGES_ORIGIN ?? DEFAULT_GITHUB_PAGES_ORIGIN).replace(/\/$/, "");
}

/**
 * Builds the upstream GitHub Pages URL for a public-site request. The public
 * host will eventually be Render, but the static site itself remains stored
 * and maintained on GitHub Pages.
 */
export function githubPagesUrl(pathAndSearch: string): URL {
  if (!pathAndSearch.startsWith("/") || /(^|\/)\.\.?(?:\/|$|\?)/.test(pathAndSearch)) {
    throw new Error("Invalid public-site path");
  }

  return new URL(`${githubPagesOrigin()}${pathAndSearch}`);
}

export function githubPagesRedirectLocation(location: string): string | null {
  const upstreamBase = new URL(githubPagesOrigin());
  const target = new URL(location, upstreamBase);
  const upstreamPrefix = upstreamBase.pathname.replace(/\/$/, "");

  if (target.origin !== upstreamBase.origin || !target.pathname.startsWith(`${upstreamPrefix}/`)) {
    return null;
  }

  return `${target.pathname.slice(upstreamPrefix.length)}${target.search}${target.hash}`;
}

export function githubPagesResponseHeaders(upstream: Headers): Headers {
  const headers = new Headers();
  for (const name of ["content-type", "cache-control", "etag", "last-modified", "content-language"]) {
    const value = upstream.get(name);
    if (value) headers.set(name, value);
  }
  return headers;
}
