import { githubPagesResponseHeaders, githubPagesUrl } from "@/lib/github-pages-proxy";

/**
 * Serves the existing static website from GitHub Pages while the same Render
 * service handles the dynamic directory and admin routes. Only GET and HEAD
 * route handlers call this function.
 */
export async function proxyGitHubPagesRequest(request: Request): Promise<Response> {
  const incoming = new URL(request.url);
  const upstreamUrl = githubPagesUrl(`${incoming.pathname}${incoming.search}`);

  try {
    const upstream = await fetch(upstreamUrl, {
      headers: {
        accept: request.headers.get("accept") ?? "*/*",
        "accept-language": request.headers.get("accept-language") ?? "",
      },
      // Follow GitHub Pages' directory canonicalisation (for example /blog →
      // /blog/) inside the server, so visitors remain on the public domain.
      redirect: "follow",
      cache: "no-store",
    });

    const headers = githubPagesResponseHeaders(upstream.headers);

    return new Response(request.method === "HEAD" ? null : upstream.body, {
      status: upstream.status,
      headers,
    });
  } catch {
    return new Response("The public site is temporarily unavailable.", {
      status: 502,
      headers: { "content-type": "text/plain; charset=utf-8", "cache-control": "no-store" },
    });
  }
}
