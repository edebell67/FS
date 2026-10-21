# Controller list - page v2.65.53 (generated 2026-10-21 from inventory_v2.65.53/inventory.json, tools/controller_wrappers.py, engine/page.py)

A controller here = a page function that is not pure logic: kind `mixed` (state + DOM), plus the delegated or ported ones. Columns: kind, async, number of fetch endpoints, DOM references, lines, page start line.


## Delegated to engine (wrapper) (29)

| Function | Kind | Async | Fetches | DOM refs | Lines | Line |
|---|---|---|---|---|---|---|
| activatePortfolio | mixed | yes |  | 2 | 180 | 4247 |
| addCatalogueModel | mixed | yes |  | 1 | 21 | 3840 |
| applyChartLock | mixed |  |  | 5 | 29 | 7195 |
| applyPortfolioViewConfig | mixed |  |  | 17 | 60 | 2441 |
| applySelectedTime | mixed |  |  | 3 | 49 | 6125 |
| autoPinLivePortfolioStrategies | engine |  |  |  | 9 | 2545 |
| capturePortfolioScenario | engine |  |  |  | 11 | 3725 |
| createSimilarPortfolio | mixed | yes |  | 3 | 25 | 4637 |
| currentPortfolioViewConfig | engine |  |  |  | 23 | 2407 |
| getMergedPortfolioModels | engine |  |  |  | 9 | 3955 |
| markPortfolioFixed | engine |  |  |  | 12 | 3737 |
| moveModelBetweenPortfolios | mixed | yes |  | 1 | 22 | 3932 |
| movePortfolio | engine |  |  |  | 13 | 2323 |
| pauseReplay | mixed |  |  | 4 | 11 | 6765 |
| persistPortfolioViewConfig | engine |  |  |  | 9 | 2431 |
| refreshActivePortfolioView | mixed | yes |  | 1 | 19 | 4199 |
| refreshLiveData | mixed | yes |  | 2 | 115 | 4832 |
| refreshPointInTimeSelection | mixed | yes | 1 | 11 | 211 | 6310 |
| removeModelFromPortfolio | engine | yes |  |  | 15 | 3762 |
| removePortfolios | engine | yes |  |  | 26 | 3793 |
| repopulateActivePortfolioFromCriteria | engine | yes |  |  | 14 | 4232 |
| resetAutomaticRankSchedule | mixed |  |  | 1 | 22 | 2076 |
| setRankingCriteria | mixed | yes |  | 5 | 146 | 5258 |
| startReplay | mixed |  |  | 4 | 13 | 6751 |
| switchDate | mixed | yes |  | 2 | 89 | 6585 |
| syncPortfolioViewRefresh | engine |  |  |  | 8 | 4219 |
| triggerSelectedTimeRefresh | mixed |  |  | 1 | 9 | 1999 |
| uniquePortfolioName | engine |  |  |  | 7 | 4629 |
| updateAutoRefreshTop1Status | view |  |  | 1 | 6 | 2040 |

## Engine call (rule logic removed from page) (12)

| Function | Kind | Async | Fetches | DOM refs | Lines | Line |
|---|---|---|---|---|---|---|
| applyAssignedOverlayTradeResults | engine |  |  |  | 67 | 2936 |
| asOfCorrelation | engine |  |  |  | 16 | 2839 |
| assignedRuleTarget | engine |  |  |  | 19 | 3004 |
| computeLeaderRotation | engine |  |  |  | 159 | 8532 |
| computeMultiSplitRotation | engine |  |  |  | 176 | 8695 |
| computeSplitTargetSignal | engine |  |  |  | 38 | 8430 |
| computeTradeOverlaySignals | engine |  |  |  | 143 | 8246 |
| curvePointAtOrBefore | engine |  |  |  | 11 | 2898 |
| overlayRuleCandidate | engine |  |  |  | 106 | 2732 |
| overlayRuleMetricValue | engine |  |  |  | 20 | 2621 |
| pairOverlayTrades | engine |  |  |  | 35 | 8392 |
| sourceTradeFlipResults | engine |  |  |  | 25 | 2910 |

## Ported in engine/page.py, NOT delegated (11)

| Function | Kind | Async | Fetches | DOM refs | Lines | Line |
|---|---|---|---|---|---|---|
| activePortfolioOverlayRule | engine |  |  |  | 4 | 2580 |
| assignedPortfolioOverlayRule | engine |  |  |  | 5 | 2574 |
| deletePortfolio | mixed | yes |  | 1 | 4 | 3778 |
| deleteSelectedPortfolios | mixed | yes |  | 1 | 9 | 3783 |
| livePortfolioModelsForDate | engine |  |  |  | 31 | 2513 |
| loadPortfolioData | engine | yes |  |  | 40 | 4095 |
| loadModelSearchFromDatabase | mixed | yes | 5 | 13 | 193 | 5761 |
| loadDeepLinkModelsFromDatabase | mixed | yes |  | 4 | 75 | 5955 |
| schedulePointInTimeSelection | mixed |  |  | 1 | 26 | 6521 |
| refreshPointInTimeHistory | mixed | yes | 1 | 4 | 26 | 6283 |
| scheduleAutomaticTop1Refresh | mixed |  |  | 2 | 47 | 6200 |

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
| getEligibleModels | mixed |  |  | 10 | 82 | 5604 |
| loadHourlyReport | mixed | yes | 1 | 15 | 36 | 6997 |
| loadLivePortfolioRulesIntoForm | mixed | yes |  | 19 | 29 | 3490 |
| loadStrategyCatalogue | mixed | yes | 1 | 2 | 19 | 3902 |
| populateCataloguePortfolioOptions | mixed |  |  | 6 | 9 | 3830 |
| restorePortfolioWorkspaceFromPostgres | mixed | yes | 1 | 1 | 26 | 2380 |
| saveLivePortfolioRules | mixed | yes | 1 | 24 | 45 | 3675 |
| saveNamedOverlayRule | mixed | yes |  | 21 | 40 | 3063 |
| savePortfolioWorkspaceToPostgres | mixed | yes | 1 | 3 | 29 | 2350 |
| scheduleDashboardUtilityRuntime | mixed |  |  | 1 | 9 | 9374 |
| setAllSectionsCollapsed | mixed |  |  | 3 | 8 | 5187 |
| setCatalogueOptions | mixed |  |  | 9 | 9 | 3820 |
| setLiveBadge | mixed |  |  | 3 | 11 | 4820 |
| setSectionCollapsed | mixed |  |  | 7 | 8 | 5161 |
| setupCanvas | mixed |  |  | 2 | 13 | 8215 |
| setupCollapsibleSections | mixed |  |  | 9 | 23 | 5196 |
| setupDateTabs | mixed |  |  | 4 | 16 | 5238 |
| setupEventListeners | mixed |  |  | 160 | 701 | 7225 |
| setupTradesModal | mixed |  |  | 23 | 18 | 5141 |
| syncHourlyProducts | mixed |  |  | 3 | 6 | 6990 |
| syncLivePortfolioScreenState | mixed | yes |  | 1 | 35 | 3639 |
| syncSplitModeControls | mixed |  |  | 7 | 19 | 5502 |
| updateCollapseAllControl | mixed |  |  | 12 | 11 | 5175 |
| updateOverlayTradeSummary | mixed |  |  | 9 | 27 | 8922 |
| updateRibbon | mixed |  |  | 24 | 86 | 7950 |
| updateStrategyFamilyOptions | mixed |  |  | 1 | 4 | 5546 |
