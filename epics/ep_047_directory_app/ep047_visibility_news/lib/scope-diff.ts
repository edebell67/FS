/** Pure diff description shared by the scope-change preview panel and its confirm action, so both name the exact same consequence. */
export function describeScopeChange(params: {
  currentTownMode: string;
  currentCategoryMode: string;
  proposedTownMode: string;
  proposedCategoryMode: string;
  disabledTownLabels: string[];
  disabledCategoryLabels: string[];
}): string[] {
  const lines: string[] = [];
  if (params.proposedTownMode !== params.currentTownMode) {
    const direction = params.proposedTownMode === "all" ? "become visible" : "become hidden (unless individually enabled)";
    lines.push(
      `Town mode ${params.currentTownMode} -> ${params.proposedTownMode}: ${params.disabledTownLabels.length} previously-disabled town(s) will ${direction}` +
        (params.disabledTownLabels.length ? ` (${params.disabledTownLabels.join(", ")})` : "")
    );
  }
  if (params.proposedCategoryMode !== params.currentCategoryMode) {
    const direction = params.proposedCategoryMode === "all" ? "become visible" : "become hidden (unless individually enabled)";
    lines.push(
      `Category mode ${params.currentCategoryMode} -> ${params.proposedCategoryMode}: ${params.disabledCategoryLabels.length} previously-disabled category(ies) will ${direction}` +
        (params.disabledCategoryLabels.length ? ` (${params.disabledCategoryLabels.join(", ")})` : "")
    );
  }
  return lines.length ? lines : ["No effective change (modes unchanged)"];
}
