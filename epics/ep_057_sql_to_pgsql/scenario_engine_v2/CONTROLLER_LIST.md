# Controller list - page v2.65.54 (generated 2026-10-22 from inventory_v2.65.54/inventory.json, tools/controller_wrappers.py, engine/page.py)

A controller here = a page function that is not pure logic: kind `mixed` (state + DOM), plus the delegated or ported ones. Columns: kind, async, number of fetch endpoints, DOM references, lines, page start line.


## Delegated to engine (wrapper) (29)

| Function | Kind | Async | Fetches | DOM refs | Lines | Line |
|---|---|---|---|---|---|---|
| activatePortfolio | mixed | yes |  | 2 | 180 | 4266 |
| addCatalogueModel | mixed | yes |  | 1 | 21 | 3852 |
| applyChartLock | mixed |  |  | 5 | 29 | 7236 |
| applyPortfolioViewConfig | mixed |  |  | 17 | 60 | 2453 |
| applySelectedTime | mixed |  |  | 3 | 49 | 6166 |
| autoPinLivePortfolioStrategies | engine |  |  |  | 9 | 2557 |
| capturePortfolioScenario | engine |  |  |  | 11 | 3737 |
| createSimilarPortfolio | mixed | yes |  | 3 | 25 | 4656 |
| currentPortfolioViewConfig | engine |  |  |  | 23 | 2419 |
| getMergedPortfolioModels | engine |  |  |  | 9 | 3967 |
| markPortfolioFixed | engine |  |  |  | 12 | 3749 |
| moveModelBetweenPortfolios | mixed | yes |  | 1 | 22 | 3944 |
| movePortfolio | engine |  |  |  | 13 | 2335 |
| pauseReplay | mixed |  |  | 4 | 11 | 6806 |
| persistPortfolioViewConfig | engine |  |  |  | 9 | 2443 |
| refreshActivePortfolioView | mixed | yes |  | 1 | 19 | 4211 |
| refreshLiveData | mixed | yes |  | 2 | 117 | 4851 |
| refreshPointInTimeSelection | mixed | yes | 1 | 11 | 211 | 6351 |
| removeModelFromPortfolio | engine | yes |  |  | 15 | 3774 |
| removePortfolios | engine | yes |  |  | 26 | 3805 |
| repopulateActivePortfolioFromCriteria | engine | yes |  |  | 14 | 4251 |
| resetAutomaticRankSchedule | mixed |  |  | 1 | 22 | 2088 |
| setRankingCriteria | mixed | yes |  | 5 | 146 | 5279 |
| startReplay | mixed |  |  | 4 | 13 | 6792 |
| switchDate | mixed | yes |  | 2 | 89 | 6626 |
| syncPortfolioViewRefresh | engine |  |  |  | 8 | 4231 |
| triggerSelectedTimeRefresh | mixed |  |  | 1 | 9 | 2003 |
| uniquePortfolioName | engine |  |  |  | 7 | 4648 |
| updateAutoRefreshTop1Status | view |  |  | 1 | 6 | 2052 |

## Engine call (rule logic removed from page) (12)

| Function | Kind | Async | Fetches | DOM refs | Lines | Line |
|---|---|---|---|---|---|---|
| applyAssignedOverlayTradeResults | engine |  |  |  | 67 | 2948 |
| asOfCorrelation | engine |  |  |  | 16 | 2851 |
| assignedRuleTarget | engine |  |  |  | 19 | 3016 |
| computeLeaderRotation | engine |  |  |  | 159 | 8566 |
| computeMultiSplitRotation | engine |  |  |  | 176 | 8729 |
| computeSplitTargetSignal | engine |  |  |  | 38 | 8460 |
| computeTradeOverlaySignals | engine |  |  |  | 143 | 8276 |
| curvePointAtOrBefore | engine |  |  |  | 11 | 2910 |
| overlayRuleCandidate | engine |  |  |  | 106 | 2744 |
| overlayRuleMetricValue | engine |  |  |  | 20 | 2633 |
| pairOverlayTrades | engine |  |  |  | 35 | 8422 |
| sourceTradeFlipResults | engine |  |  |  | 25 | 2922 |

## Ported in engine/page.py, NOT delegated (11)

| Function | Kind | Async | Fetches | DOM refs | Lines | Line |
|---|---|---|---|---|---|---|
| activePortfolioOverlayRule | engine |  |  |  | 4 | 2592 |
| assignedPortfolioOverlayRule | engine |  |  |  | 5 | 2586 |
| deletePortfolio | mixed | yes |  | 1 | 4 | 3790 |
| deleteSelectedPortfolios | mixed | yes |  | 1 | 9 | 3795 |
| livePortfolioModelsForDate | engine |  |  |  | 31 | 2525 |
| loadPortfolioData | engine | yes |  |  | 40 | 4107 |
| loadModelSearchFromDatabase | mixed | yes | 5 | 13 | 193 | 5793 |
| loadDeepLinkModelsFromDatabase | mixed | yes |  | 4 | 75 | 5987 |
| schedulePointInTimeSelection | mixed |  |  | 1 | 26 | 6562 |
| refreshPointInTimeHistory | mixed | yes | 1 | 4 | 26 | 6324 |
| scheduleAutomaticTop1Refresh | mixed |  |  | 2 | 47 | 6241 |

## Stays in page (34)

| Function | Kind | Async | Fetches | DOM refs | Lines | Line |
|---|---|---|---|---|---|---|
| activateLiveModeFromReview | mixed | yes | 1 | 38 | 93 | 3357 |
| appendRuleDetailsSection | mixed |  |  | 18 | 30 | 3558 |
| applyDisplayTheme | mixed |  |  | 9 | 11 | 3762 |
| assignOverlayRule | mixed | yes | 1 | 8 | 24 | 3116 |
| beginEditNamedOverlayRule | mixed |  |  | 33 | 28 | 2707 |
| cancelEditNamedOverlayRule | mixed |  |  | 9 | 7 | 2736 |
| configFromOverlayEditor | mixed |  |  | 16 | 16 | 3042 |
| editLivePortfolioRules | mixed | yes |  | 9 | 8 | 3642 |
| getEligibleModels | mixed |  |  | 10 | 90 | 5626 |
| loadHourlyReport | mixed | yes | 1 | 15 | 36 | 7038 |
| loadLivePortfolioRulesIntoForm | mixed | yes |  | 19 | 29 | 3502 |
| loadStrategyCatalogue | mixed | yes | 1 | 2 | 19 | 3914 |
| populateCataloguePortfolioOptions | mixed |  |  | 6 | 9 | 3842 |
| restorePortfolioWorkspaceFromPostgres | mixed | yes | 1 | 1 | 26 | 2392 |
| saveLivePortfolioRules | mixed | yes | 1 | 24 | 45 | 3687 |
| saveNamedOverlayRule | mixed | yes |  | 21 | 40 | 3075 |
| savePortfolioWorkspaceToPostgres | mixed | yes | 1 | 3 | 29 | 2362 |
| scheduleDashboardUtilityRuntime | mixed |  |  | 1 | 9 | 9408 |
| setAllSectionsCollapsed | mixed |  |  | 3 | 8 | 5208 |
| setCatalogueOptions | mixed |  |  | 9 | 9 | 3832 |
| setLiveBadge | mixed |  |  | 3 | 11 | 4839 |
| setSectionCollapsed | mixed |  |  | 7 | 8 | 5182 |
| setupCanvas | mixed |  |  | 2 | 13 | 8245 |
| setupCollapsibleSections | mixed |  |  | 9 | 23 | 5217 |
| setupDateTabs | mixed |  |  | 4 | 16 | 5259 |
| setupEventListeners | mixed |  |  | 160 | 701 | 7266 |
| setupTradesModal | mixed |  |  | 23 | 18 | 5162 |
| syncHourlyProducts | mixed |  |  | 3 | 6 | 7031 |
| syncLivePortfolioScreenState | mixed | yes |  | 1 | 35 | 3651 |
| syncSplitModeControls | mixed |  |  | 7 | 19 | 5524 |
| updateCollapseAllControl | mixed |  |  | 12 | 11 | 5196 |
| updateOverlayTradeSummary | mixed |  |  | 9 | 27 | 8956 |
| updateRibbon | mixed |  |  | 24 | 86 | 7991 |
| updateStrategyFamilyOptions | mixed |  |  | 1 | 4 | 5568 |
