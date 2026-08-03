import assert from "node:assert/strict";
import test from "node:test";
import { describeScopeChange } from "./lib/scope-diff";

test("no mode change reports no effective change", () => {
  const lines = describeScopeChange({
    currentTownMode: "all",
    currentCategoryMode: "all",
    proposedTownMode: "all",
    proposedCategoryMode: "all",
    disabledTownLabels: ["Manchester"],
    disabledCategoryLabels: [],
  });
  assert.deepEqual(lines, ["No effective change (modes unchanged)"]);
});

test("selected -> all names the previously-disabled towns that become visible", () => {
  const lines = describeScopeChange({
    currentTownMode: "selected",
    currentCategoryMode: "all",
    proposedTownMode: "all",
    proposedCategoryMode: "all",
    disabledTownLabels: ["Manchester", "Birmingham"],
    disabledCategoryLabels: [],
  });
  assert.equal(lines.length, 1);
  const [first] = lines;
  assert.ok(first);
  assert.match(first, /Town mode selected -> all/);
  assert.match(first, /become visible/);
  assert.match(first, /Manchester, Birmingham/);
});

test("all -> selected names the towns that become hidden, and reports zero when none are disabled", () => {
  const lines = describeScopeChange({
    currentTownMode: "all",
    currentCategoryMode: "all",
    proposedTownMode: "selected",
    proposedCategoryMode: "all",
    disabledTownLabels: [],
    disabledCategoryLabels: [],
  });
  assert.equal(lines.length, 1);
  const [first] = lines;
  assert.ok(first);
  assert.match(first, /become hidden/);
  assert.match(first, /^Town mode all -> selected: 0 previously-disabled town\(s\)/);
});

test("both dimensions changing produce two independent lines", () => {
  const lines = describeScopeChange({
    currentTownMode: "selected",
    currentCategoryMode: "selected",
    proposedTownMode: "all",
    proposedCategoryMode: "all",
    disabledTownLabels: ["Manchester"],
    disabledCategoryLabels: ["Hairdressers"],
  });
  assert.equal(lines.length, 2);
  const [first, second] = lines;
  assert.ok(first);
  assert.ok(second);
  assert.match(first, /^Town mode/);
  assert.match(second, /^Category mode/);
  assert.match(second, /Hairdressers/);
});
