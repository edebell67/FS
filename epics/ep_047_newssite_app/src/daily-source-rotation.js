import { NEWS_SOURCE_REGISTRY, SOURCE_REGISTRY_VERSION, validateSourceRegistry } from "./source-registry.js";

function isoDay(date) {
  const normalized = typeof date === "string" ? date : date.toISOString().slice(0, 10);
  if (!/^\d{4}-\d{2}-\d{2}$/.test(normalized) || Number.isNaN(Date.parse(`${normalized}T00:00:00Z`))) throw new Error("A valid UTC YYYY-MM-DD date is required.");
  return normalized;
}

function dayNumber(date) {
  return Math.floor(Date.parse(`${date}T00:00:00Z`) / 86_400_000);
}

/** Pure coverage plan. A plan does no network, file, DB or intake work. */
export function buildDailySourcePlan({ date, eligibleTowns, registry = NEWS_SOURCE_REGISTRY }) {
  validateSourceRegistry(registry);
  const runDate = isoDay(date);
  const towns = [...new Set((eligibleTowns || []).map((town) => typeof town === "string" ? town : town.slug).filter(Boolean))].sort();
  const selections = [];
  const uncoveredTowns = [];
  for (const town of towns) {
    const sources = registry.filter((source) => source.status === "enabled" && source.towns.includes(town)).sort((a, b) => a.id.localeCompare(b.id));
    if (!sources.length) { uncoveredTowns.push(town); continue; }
    selections.push({ town, sourceId: sources[dayNumber(runDate) % sources.length].id });
  }
  return Object.freeze({ version: "ep047.daily-source-plan/v1", registryVersion: SOURCE_REGISTRY_VERSION, date: runDate, selections, uncoveredTowns });
}
