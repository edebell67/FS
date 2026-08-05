/**
 * Guards for the site-generation completion seam.
 * Generated previews are served through the customer-facing proxy, never an
 * arbitrary deployment URL or a direct upstream host.
 */

export const DEFAULT_CUSTOMER_PROXY_HOSTNAMES = ["thetechprinciple.com"] as const;

function configuredCustomerProxyHostnames(
  environment: { CUSTOMER_PROXY_HOSTNAMES?: string | undefined } = process.env as { CUSTOMER_PROXY_HOSTNAMES?: string | undefined },
): readonly string[] {
  const configured = environment.CUSTOMER_PROXY_HOSTNAMES
    ?.split(",")
    .map((hostname) => hostname.trim().toLowerCase())
    .filter(Boolean);

  return configured?.length ? configured : DEFAULT_CUSTOMER_PROXY_HOSTNAMES;
}

/** Parses and restricts a generated-site URL to an approved HTTPS proxy host. */
export function assertApprovedCustomerProxyUrl(
  rawUrl: string,
  allowedHostnames: readonly string[] = configuredCustomerProxyHostnames(),
): URL {
  let url: URL;
  try {
    url = new URL(rawUrl);
  } catch {
    throw new Error("Generated site URL must be a valid absolute HTTPS URL.");
  }

  if (url.protocol !== "https:") {
    throw new Error("Generated site URL must use HTTPS.");
  }
  if (url.username || url.password || url.port) {
    throw new Error("Generated site URL must not include credentials or a port.");
  }

  const approved = new Set(allowedHostnames.map((hostname) => hostname.toLowerCase()));
  if (!approved.has(url.hostname.toLowerCase())) {
    throw new Error("Generated site URL must use an approved customer proxy hostname.");
  }

  return url;
}

/**
 * Confirms that the approved public URL is serving successfully before a
 * database stage can be advanced. Redirects are deliberately not followed:
 * the asserted customer-proxy URL itself must be live.
 */
export async function verifyGeneratedSiteUrl(
  rawUrl: string,
  fetchImpl: typeof fetch = fetch,
): Promise<URL> {
  const url = assertApprovedCustomerProxyUrl(rawUrl);
  let response: Response;
  try {
    response = await fetchImpl(url, {
      method: "GET",
      headers: { accept: "text/html,application/xhtml+xml" },
      redirect: "manual",
      cache: "no-store",
      signal: AbortSignal.timeout(10_000),
    });
  } catch {
    throw new Error("Generated site URL could not be verified live.");
  }

  if (!response.ok) {
    throw new Error(`Generated site URL did not verify live (HTTP ${response.status}).`);
  }

  return url;
}
