import test from "node:test";
import assert from "node:assert/strict";
import { resolveNewsDirectoryLink } from "@/ep047_visibility_news/lib/public-links";

test("news links prefer an eligible town/category route", () => {
  assert.equal(resolveNewsDirectoryLink({ town: "Birmingham", categories: ["Hairdressers"], publicTowns: ["birmingham"], publicCategories: ["hairdressers"] }), "/directory/town/birmingham?category=Hairdressers");
});

test("news links fall back to the eligible town when category is unavailable", () => {
  assert.equal(resolveNewsDirectoryLink({ town: "Birmingham", categories: ["Retail"], publicTowns: ["Birmingham"], publicCategories: ["Hairdressers"] }), "/directory/town/birmingham");
});

test("news links are omitted when the town is hidden", () => {
  assert.equal(resolveNewsDirectoryLink({ town: "Birmingham", categories: ["Hairdressers"], publicTowns: ["Manchester"], publicCategories: ["Hairdressers"] }), null);
});
