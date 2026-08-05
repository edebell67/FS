import test from "node:test";
import assert from "node:assert/strict";
import { NEWS_SOURCE_REGISTRY, enabledSourcesForTown, sourceAllowsUrl, validateSourceRegistry } from "../src/source-registry.js";

test("registry has uniquely identified, curator-approved enabled sources", () => {
  assert.doesNotThrow(() => validateSourceRegistry());
  assert.deepEqual(enabledSourcesForTown("bristol").map((source) => source.id), ["bristol-city-council-news"]);
  assert.deepEqual(enabledSourcesForTown("leeds").map((source) => source.id), ["leeds-city-council-news"]);
  assert.equal(NEWS_SOURCE_REGISTRY.filter((source) => source.status === "draft").length, 3);
});

test("source URLs must remain on the source's approved host", () => {
  const bristol = NEWS_SOURCE_REGISTRY.find((source) => source.id === "bristol-city-council-news");
  assert.equal(sourceAllowsUrl(bristol, "https://news.bristol.gov.uk/press-releases/example"), true);
  assert.equal(sourceAllowsUrl(bristol, "https://example.invalid/press-releases/example"), false);
});
