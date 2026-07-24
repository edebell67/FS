const DEFAULT_GITHUB_PAGES_ORIGIN = "https://edebell67.github.io/FS";

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
