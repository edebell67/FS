/**
 * Human-curated EP047 News source registry.
 *
 * Only enabled records form a daily coverage obligation. Draft sources are
 * discovery candidates and cannot be scanned or described as covered until a
 * curator confirms access/terms, town relevance and review date.
 */
const requiredKinds = new Set(["official_council", "official_combined_authority", "business_improvement_district", "official_destination"]);

export const SOURCE_REGISTRY_VERSION = "2026-08-05.1";

export const NEWS_SOURCE_REGISTRY = Object.freeze([
  {
    id: "bristol-city-council-news",
    status: "enabled",
    name: "Bristol City Council Newsroom",
    publisher: "Bristol City Council",
    kind: "official_council",
    towns: ["bristol"],
    allowedHosts: ["news.bristol.gov.uk"],
    discovery: { mode: "manual_research", url: "https://news.bristol.gov.uk/" },
    coverage: { categories: ["builders", "carpenters", "fencing", "handyman", "mobile mechanics", "carpet cleaners", "estate agents", "marketing agencies", "photographers", "web design"], priority: "primary" },
    termsDecision: "permitted_link_and_fact_extraction",
    termsCheckedAt: "2026-08-05",
    reviewDueAt: "2026-11-05",
  },
  {
    id: "leeds-city-council-news",
    status: "enabled",
    name: "Leeds City Council News",
    publisher: "Leeds City Council",
    kind: "official_council",
    towns: ["leeds"],
    allowedHosts: ["news.leeds.gov.uk"],
    discovery: { mode: "manual_research", url: "https://news.leeds.gov.uk/news" },
    coverage: { categories: ["architects", "builders", "carpenters", "kitchen fitters", "barbers", "beauty salons", "photographers"], priority: "primary" },
    termsDecision: "permitted_link_and_fact_extraction",
    termsCheckedAt: "2026-08-05",
    reviewDueAt: "2026-11-05",
  },
  // Freshly verified discovery candidates. Deliberately draft: human curation
  // must record access/terms before they become coverage obligations.
  {
    id: "leeds-bid-news",
    status: "draft",
    name: "LeedsBID Latest News",
    publisher: "LeedsBID",
    kind: "business_improvement_district",
    towns: ["leeds"],
    allowedHosts: ["www.leedsbid.co.uk"],
    discovery: { mode: "manual_research", url: "https://www.leedsbid.co.uk/news/" },
    coverage: { categories: ["retailers", "hospitality", "events", "marketing agencies"], priority: "supplementary" },
    termsDecision: "curator_review_required",
    termsCheckedAt: null,
    reviewDueAt: null,
  },
  {
    id: "west-of-england-combined-authority-news",
    status: "draft",
    name: "West of England Combined Authority Latest News",
    publisher: "West of England Combined Authority",
    kind: "official_combined_authority",
    towns: ["bristol"],
    allowedHosts: ["www.westofengland-ca.gov.uk"],
    discovery: { mode: "manual_research", url: "https://www.westofengland-ca.gov.uk/news/" },
    coverage: { categories: ["transport", "planning", "housing", "business support", "skills"], priority: "supplementary" },
    termsDecision: "curator_review_required",
    termsCheckedAt: null,
    reviewDueAt: null,
  },
  {
    id: "visit-bristol-events",
    status: "draft",
    name: "Visit Bristol What's On",
    publisher: "Visit Bristol",
    kind: "official_destination",
    towns: ["bristol"],
    allowedHosts: ["visitbristol.co.uk", "www.visitbristol.co.uk"],
    discovery: { mode: "manual_research", url: "https://visitbristol.co.uk/whats-on/" },
    coverage: { categories: ["events", "hospitality", "photographers", "retailers"], priority: "supplementary" },
    termsDecision: "curator_review_required",
    termsCheckedAt: null,
    reviewDueAt: null,
  },
]);

export function validateSourceRegistry(registry = NEWS_SOURCE_REGISTRY) {
  const ids = new Set();
  for (const source of registry) {
    if (!source || !source.id || ids.has(source.id)) throw new Error("News source registry IDs must be unique.");
    ids.add(source.id);
    if (!requiredKinds.has(source.kind)) throw new Error(`News source ${source.id} has an unsupported kind.`);
    if (!["draft", "enabled", "paused", "retired"].includes(source.status)) throw new Error(`News source ${source.id} has an invalid status.`);
    if (!source.towns?.length || !source.allowedHosts?.length || !source.discovery?.url || !source.coverage?.categories?.length) throw new Error(`News source ${source.id} is incomplete.`);
    if (source.status === "enabled" && (!source.termsCheckedAt || source.termsDecision !== "permitted_link_and_fact_extraction")) throw new Error(`Enabled source ${source.id} lacks curator terms approval.`);
  }
  return registry;
}

export function enabledSourcesForTown(town, registry = NEWS_SOURCE_REGISTRY) {
  validateSourceRegistry(registry);
  return registry.filter((source) => source.status === "enabled" && source.towns.includes(town));
}

export function sourceAllowsUrl(source, url) {
  const hostname = new URL(url).hostname.toLowerCase();
  return source.allowedHosts.includes(hostname);
}
