# Controller list - page v2.65.53 (generated 2026-10-21 from inventory_v2.65.53/inventory.json, tools/controller_wrappers.py, engine/page.py)

A controller here = a page function that is not pure logic: kind `mixed` (state + DOM), plus the delegated or ported ones. Columns: kind, async, number of fetch endpoints, DOM references, lines, page start line.


## Delegated to engine (wrapper) (29)

| Function | Kind | Async | Fetches | DOM refs | Lines | Line |
|---|---|---|---|---|---|---|
| activatePortfolio | mixed | yes |  | 2 | 177 | 4246 |
| addCatalogueModel | mixed | yes |  | 1 | 21 | 3840 |
| applyChartLock | mixed |  |  | 5 | 29 | 7184 |
| applyPortfolioViewConfig | mixed |  |  | 17 | 60 | 2441 |
| applySelectedTime | mixed |  |  | 5 | 53 | 6110 |
| autoPinLivePortfolioStrategies | engine |  |  |  | 9 | 2545 |
| capturePortfolioScenario | engine |  |  |  | 11 | 3725 |
| createSimilarPortfolio | mixed | yes |  | 3 | 25 | 4633 |
| currentPortfolioViewConfig | engine |  |  |  | 23 | 2407 |
| getMergedPortfolioModels | engine |  |  |  | 9 | 3955 |
| markPortfolioFixed | engine |  |  |  | 12 | 3737 |
| moveModelBetweenPortfolios | mixed | yes |  | 1 | 22 | 3932 |
| movePortfolio | engine |  |  |  | 13 | 2323 |
| pauseReplay | mixed |  |  | 4 | 11 | 6754 |
| persistPortfolioViewConfig | engine |  |  |  | 9 | 2431 |
| refreshActivePortfolioView | mixed | yes |  | 1 | 19 | 4198 |
| refreshLiveData | mixed | yes |  | 2 | 115 | 4828 |
| refreshPointInTimeSelection | mixed | yes | 1 | 11 | 211 | 6299 |
| removeModelFromPortfolio | engine | yes |  |  | 15 | 3762 |
| removePortfolios | engine | yes |  |  | 26 | 3793 |
| repopulateActivePortfolioFromCriteria | engine | yes |  |  | 14 | 4231 |
| resetAutomaticRankSchedule | mixed |  |  | 1 | 22 | 2076 |
| setRankingCriteria | mixed | yes |  | 5 | 146 | 5254 |
| startReplay | mixed |  |  | 4 | 13 | 6740 |
| switchDate | mixed | yes |  | 2 | 89 | 6574 |
| syncPortfolioViewRefresh | engine |  |  |  | 8 | 4218 |
| triggerSelectedTimeRefresh | mixed |  |  | 1 | 9 | 1999 |
| uniquePortfolioName | engine |  |  |  | 7 | 4625 |
| updateAutoRefreshTop1Status | view |  |  | 1 | 6 | 2040 |

## Engine call (rule logic removed from page) (12)

| Function | Kind | Async | Fetches | DOM refs | Lines | Line |
|---|---|---|---|---|---|---|
| applyAssignedOverlayTradeResults | engine |  |  |  | 67 | 2936 |
| asOfCorrelation | engine |  |  |  | 16 | 2839 |
| assignedRuleTarget | engine |  |  |  | 19 | 3004 |
| computeLeaderRotation | engine |  |  |  | 159 | 8525 |
| computeMultiSplitRotation | engine |  |  |  | 176 | 8688 |
| computeSplitTargetSignal | engine |  |  |  | 38 | 8423 |
| computeTradeOverlaySignals | engine |  |  |  | 143 | 8239 |
| curvePointAtOrBefore | engine |  |  |  | 11 | 2898 |
| overlayRuleCandidate | engine |  |  |  | 106 | 2732 |
| overlayRuleMetricValue | engine |  |  |  | 20 | 2621 |
| pairOverlayTrades | engine |  |  |  | 35 | 8385 |
| sourceTradeFlipResults | engine |  |  |  | 25 | 2910 |

## Ported in engine/page.py, NOT delegated (11)

| Function | Kind | Async | Fetches | DOM refs | Lines | Line |
|---|---|---|---|---|---|---|
| activePortfolioOverlayRule | engine |  |  |  | 4 | 2580 |
| assignedPortfolioOverlayRule | engine |  |  |  | 5 | 2574 |
| deletePortfolio | mixed | yes |  | 1 | 4 | 3778 |
| deleteSelectedPortfolios | mixed | yes |  | 1 | 9 | 3783 |
| livePortfolioModelsForDate | engine |  |  |  | 31 | 2513 |
| loadPortfolioData | engine | yes |  |  | 40 | 4094 |
| loadModelSearchFromDatabase | mixed | yes | 5 | 13 | 193 | 5746 |
| loadDeepLinkModelsFromDatabase | mixed | yes |  | 4 | 75 | 5940 |
| schedulePointInTimeSelection | mixed |  |  | 1 | 26 | 6510 |
| refreshPointInTimeHistory | mixed | yes | 1 | 4 | 26 | 6272 |
| scheduleAutomaticTop1Refresh | mixed |  |  | 2 | 47 | 6189 |

## Stays in page (34)

| Function | Kind | Async | Fetches | DOM refs | Lines | Line |
|---|---|---|---|---|---|---|
| activateLiveModeFromReview | mixed | yes | 1 | 38 | 93 | 3345 |
| appendRuleDetailsSection | mixed |  |  | 18 | 30 | 3546 |
| applyDisplayTheme | mixed |  |  | 9 | 11 | 3750 |
| assignOverlayRule | mixed | yes | 1 | 8 | 24 | 3104 |
| beginEditNamedOverlayRule | mixed |  |  | 33 | 28 | 2695 |
| cancelEditNamedOverlayRule | mixed |  |  | 9 | 7 | 2724 |
| configFromOverlayEditor | mixed |  |  | 16 | 16 | 3030 |
| editLivePortfolioRules | mixed | yes |  | 9 | 8 | 3630 |
| getEligibleModels | mixed |  |  | 10 | 82 | 5589 |
| loadHourlyReport | mixed | yes | 1 | 15 | 36 | 6986 |
| loadLivePortfolioRulesIntoForm | mixed | yes |  | 19 | 29 | 3490 |
| loadStrategyCatalogue | mixed | yes | 1 | 2 | 19 | 3902 |
| populateCataloguePortfolioOptions | mixed |  |  | 6 | 9 | 3830 |
| restorePortfolioWorkspaceFromPostgres | mixed | yes | 1 | 1 | 26 | 2380 |
| saveLivePortfolioRules | mixed | yes | 1 | 24 | 45 | 3675 |
| saveNamedOverlayRule | mixed | yes |  | 21 | 40 | 3063 |
| savePortfolioWorkspaceToPostgres | mixed | yes | 1 | 3 | 29 | 2350 |
| scheduleDashboardUtilityRuntime | mixed |  |  | 1 | 9 | 9367 |
| setAllSectionsCollapsed | mixed |  |  | 3 | 8 | 5183 |
| setCatalogueOptions | mixed |  |  | 9 | 9 | 3820 |
| setLiveBadge | mixed |  |  | 3 | 11 | 4816 |
| setSectionCollapsed | mixed |  |  | 7 | 8 | 5157 |
| setupCanvas | mixed |  |  | 2 | 13 | 8208 |
| setupCollapsibleSections | mixed |  |  | 9 | 23 | 5192 |
| setupDateTabs | mixed |  |  | 4 | 16 | 5234 |
| setupEventListeners | mixed |  |  | 162 | 707 | 7214 |
| setupTradesModal | mixed |  |  | 23 | 18 | 5137 |
| syncHourlyProducts | mixed |  |  | 3 | 6 | 6979 |
| syncLivePortfolioScreenState | mixed | yes |  | 1 | 35 | 3639 |
| syncSplitModeControls | mixed |  |  | 7 | 19 | 5498 |
| updateCollapseAllControl | mixed |  |  | 12 | 11 | 5171 |
| updateOverlayTradeSummary | mixed |  |  | 9 | 27 | 8915 |
| updateRibbon | mixed |  |  | 24 | 86 | 7945 |
| updateStrategyFamilyOptions | mixed |  |  | 1 | 4 | 5542 |
