// Single source for the site's public base URL — used for canonical links,
// sitemap entries, and JSON-LD `item`/`url` fields. Set NEXT_PUBLIC_SITE_URL
// once this deploys to Render; falls back to localhost for dev.
export const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:8140";
export const SITE_NAME = "The Directory";
