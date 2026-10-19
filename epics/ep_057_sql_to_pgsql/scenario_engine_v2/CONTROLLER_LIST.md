# Controller list - page v2.65.34 (generated 2026-10-19 from inventory_v2.65.34/inventory.json, tools/controller_wrappers.py, engine/page.py)

A controller here = a page function that is not pure logic: kind `mixed` (state + DOM), plus the delegated or ported ones. Columns: kind, async, number of fetch endpoints, DOM references, lines, page start line.


## Delegated to engine (wrapper) (32)

| Function | Kind | Async | Fetches | DOM refs | Lines | Line |
|---|---|---|---|---|---|---|
| activatePortfolio | mixed | yes |  | 2 | 177 | 4137 |
| addCatalogueModel | mixed | yes |  | 1 | 21 | 3731 |
| applyChartLock | mixed |  |  | 5 | 29 | 6692 |
| applyPortfolioViewConfig | mixed |  |  | 17 | 60 | 2334 |
| applySelectedTime | mixed |  |  | 5 | 53 | 5744 |
| autoPinLivePortfolioStrategies | engine |  |  |  | 9 | 2438 |
| capturePortfolioScenario | engine |  |  |  | 11 | 3616 |
| createSimilarPortfolio | mixed | yes |  | 3 | 25 | 4524 |
| currentPortfolioViewConfig | engine |  |  |  | 23 | 2300 |
| getMergedPortfolioModels | engine |  |  |  | 9 | 3846 |
| markPortfolioFixed | engine |  |  |  | 12 | 3628 |
| moveModelBetweenPortfolios | mixed | yes |  | 1 | 22 | 3823 |
| movePortfolio | engine |  |  |  | 13 | 2216 |
| pauseReplay | mixed |  |  | 4 | 11 | 6388 |
| persistPortfolioViewConfig | engine |  |  |  | 9 | 2324 |
| refreshActivePortfolioView | mixed | yes |  | 1 | 19 | 4089 |
| refreshLiveData | mixed | yes |  | 2 | 115 | 4721 |
| refreshPointInTimeHistory | mixed | yes | 1 | 4 | 26 | 5906 |
| refreshPointInTimeSelection | mixed | yes | 1 | 11 | 211 | 5933 |
| removeModelFromPortfolio | engine | yes |  |  | 15 | 3653 |
| removePortfolios | engine | yes |  |  | 26 | 3684 |
| repopulateActivePortfolioFromCriteria | engine | yes |  |  | 14 | 4122 |
| resetAutomaticRankSchedule | mixed |  |  | 1 | 22 | 1987 |
| scheduleAutomaticTop1Refresh | mixed |  |  | 2 | 47 | 5823 |
| schedulePointInTimeSelection | mixed |  |  | 1 | 26 | 6144 |
| setRankingCriteria | mixed | yes |  | 5 | 146 | 5147 |
| startReplay | mixed |  |  | 4 | 13 | 6374 |
| switchDate | mixed | yes |  | 2 | 89 | 6208 |
| syncPortfolioViewRefresh | engine |  |  |  | 8 | 4109 |
| triggerSelectedTimeRefresh | mixed |  |  | 1 | 9 | 1910 |
| uniquePortfolioName | engine |  |  |  | 7 | 4516 |
| updateAutoRefreshTop1Status | view |  |  | 1 | 6 | 1951 |

## Engine call (rule logic removed from page) (12)

| Function | Kind | Async | Fetches | DOM refs | Lines | Line |
|---|---|---|---|---|---|---|
| applyAssignedOverlayTradeResults | engine |  |  |  | 67 | 2829 |
| asOfCorrelation | engine |  |  |  | 16 | 2732 |
| assignedRuleTarget | engine |  |  |  | 19 | 2897 |
| computeLeaderRotation | engine |  |  |  | 159 | 7899 |
| computeMultiSplitRotation | engine |  |  |  | 176 | 8062 |
| computeSplitTargetSignal | engine |  |  |  | 38 | 7830 |
| computeTradeOverlaySignals | engine |  |  |  | 143 | 7646 |
| curvePointAtOrBefore | engine |  |  |  | 11 | 2791 |
| overlayRuleCandidate | engine |  |  |  | 106 | 2625 |
| overlayRuleMetricValue | engine |  |  |  | 20 | 2514 |
| pairOverlayTrades | engine |  |  |  | 35 | 7792 |
| sourceTradeFlipResults | engine |  |  |  | 25 | 2803 |

## Ported in engine/page.py, NOT delegated (8)

| Function | Kind | Async | Fetches | DOM refs | Lines | Line |
|---|---|---|---|---|---|---|
| activePortfolioOverlayRule | engine |  |  |  | 4 | 2473 |
| assignedPortfolioOverlayRule | engine |  |  |  | 5 | 2467 |
| deletePortfolio | mixed | yes |  | 1 | 4 | 3669 |
| deleteSelectedPortfolios | mixed | yes |  | 1 | 9 | 3674 |
| livePortfolioModelsForDate | engine |  |  |  | 31 | 2406 |
| loadPortfolioData | engine | yes |  |  | 40 | 3985 |
| loadModelSearchFromDatabase | mixed | yes | 1 | 6 | 57 | 5551 |
| loadDeepLinkModelsFromDatabase | mixed | yes | 1 | 4 | 46 | 5609 |

## Stays in page (34)

| Function | Kind | Async | Fetches | DOM refs | Lines | Line |
|---|---|---|---|---|---|---|
| activateLiveModeFromReview | mixed | yes | 1 | 38 | 93 | 3236 |
| appendRuleDetailsSection | mixed |  |  | 18 | 30 | 3437 |
| applyDisplayTheme | mixed |  |  | 9 | 11 | 3641 |
| assignOverlayRule | mixed | yes | 1 | 8 | 24 | 2997 |
| beginEditNamedOverlayRule | mixed |  |  | 33 | 28 | 2588 |
| cancelEditNamedOverlayRule | mixed |  |  | 9 | 7 | 2617 |
| configFromOverlayEditor | mixed |  |  | 16 | 16 | 2923 |
| editLivePortfolioRules | mixed | yes |  | 9 | 8 | 3521 |
| getEligibleModels | mixed |  |  | 8 | 62 | 5478 |
| loadHourlyReport | mixed | yes | 1 | 15 | 36 | 6620 |
| loadLivePortfolioRulesIntoForm | mixed | yes |  | 19 | 29 | 3381 |
| loadStrategyCatalogue | mixed | yes | 1 | 2 | 19 | 3793 |
| populateCataloguePortfolioOptions | mixed |  |  | 6 | 9 | 3721 |
| restorePortfolioWorkspaceFromPostgres | mixed | yes | 1 | 1 | 26 | 2273 |
| saveLivePortfolioRules | mixed | yes | 1 | 24 | 45 | 3566 |
| saveNamedOverlayRule | mixed | yes |  | 21 | 40 | 2956 |
| savePortfolioWorkspaceToPostgres | mixed | yes | 1 | 3 | 29 | 2243 |
| scheduleDashboardUtilityRuntime | mixed |  |  | 1 | 9 | 8732 |
| setAllSectionsCollapsed | mixed |  |  | 3 | 8 | 5076 |
| setCatalogueOptions | mixed |  |  | 9 | 9 | 3711 |
| setLiveBadge | mixed |  |  | 3 | 11 | 4709 |
| setSectionCollapsed | mixed |  |  | 7 | 8 | 5050 |
| setupCanvas | mixed |  |  | 2 | 13 | 7615 |
| setupCollapsibleSections | mixed |  |  | 9 | 23 | 5085 |
| setupDateTabs | mixed |  |  | 4 | 16 | 5127 |
| setupEventListeners | mixed |  |  | 150 | 632 | 6722 |
| setupTradesModal | mixed |  |  | 23 | 18 | 5030 |
| syncHourlyProducts | mixed |  |  | 3 | 6 | 6613 |
| syncLivePortfolioScreenState | mixed | yes |  | 1 | 35 | 3530 |
| syncSplitModeControls | mixed |  |  | 7 | 19 | 5387 |
| updateCollapseAllControl | mixed |  |  | 12 | 11 | 5064 |
| updateOverlayTradeSummary | mixed |  |  | 9 | 27 | 8289 |
| updateRibbon | mixed |  |  | 24 | 86 | 7378 |
| updateStrategyFamilyOptions | mixed |  |  | 1 | 4 | 5431 |
