// Generated business sites live in the separate github.com/edebell67/epics
// repo (flat, top-level <slug>/ folders), not the FS monorepo this app
// itself lives in -- confirmed 2026-07-31 against the working example
// dg-maintenance-uk-ltd/.
//
// This uses jsDelivr's GitHub CDN rather than GitHub Pages directly.
// GitHub Pages for that repo still has a stale custom-domain setting
// (thetechprinciple.com, which now points at Render) that 301-redirects the
// raw github.io URL even after the repo's CNAME file was deleted -- GitHub's
// side didn't clear on its own in time. jsDelivr serves the exact same repo
// content immediately with no such redirect (@master pins the branch; drop
// the pin if latest-on-push is preferred over jsDelivr's CDN cache window).
// jsDelivr reports .html/.js/.css as text/plain, which is why
// githubPagesResponseHeaders() below infers content-type from the request
// path's extension rather than trusting upstream's header.
const DEFAULT_GITHUB_PAGES_ORIGIN = "https://cdn.jsdelivr.net/gh/edebell67/epics@master";

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

const EXTENSION_CONTENT_TYPES: Record<string, string> = {
  html: "text/html; charset=utf-8",
  htm: "text/html; charset=utf-8",
  css: "text/css; charset=utf-8",
  js: "application/javascript; charset=utf-8",
  json: "application/json; charset=utf-8",
  svg: "image/svg+xml",
  png: "image/png",
  jpg: "image/jpeg",
  jpeg: "image/jpeg",
  webp: "image/webp",
  gif: "image/gif",
  ico: "image/x-icon",
  woff: "font/woff",
  woff2: "font/woff2",
  txt: "text/plain; charset=utf-8",
  xml: "application/xml; charset=utf-8",
};

/**
 * pathname is optional only for backward compatibility with any other
 * caller; every real proxy request should pass it, since jsDelivr's
 * reported content-type can't be trusted (see DEFAULT_GITHUB_PAGES_ORIGIN
 * above) and extension-based inference is what makes pages actually render.
 */
export function githubPagesResponseHeaders(upstream: Headers, pathname?: string): Headers {
  const headers = new Headers();
  for (const name of ["cache-control", "etag", "last-modified", "content-language"]) {
    const value = upstream.get(name);
    if (value) headers.set(name, value);
  }

  const extension = pathname?.split(".").pop()?.toLowerCase();
  const inferredType = extension ? EXTENSION_CONTENT_TYPES[extension] : undefined;
  const contentType = inferredType ?? upstream.get("content-type");
  if (contentType) headers.set("content-type", contentType);

  return headers;
}
