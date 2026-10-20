# Controller list - page v2.65.38 (generated 2026-10-20 from inventory_v2.65.38/inventory.json, tools/controller_wrappers.py, engine/page.py)

A controller here = a page function that is not pure logic: kind `mixed` (state + DOM), plus the delegated or ported ones. Columns: kind, async, number of fetch endpoints, DOM references, lines, page start line.


## Delegated to engine (wrapper) (29)

| Function | Kind | Async | Fetches | DOM refs | Lines | Line |
|---|---|---|---|---|---|---|
| activatePortfolio | mixed | yes |  | 2 | 177 | 4195 |
| addCatalogueModel | mixed | yes |  | 1 | 21 | 3789 |
| applyChartLock | mixed |  |  | 5 | 29 | 6889 |
| applyPortfolioViewConfig | mixed |  |  | 17 | 60 | 2392 |
| applySelectedTime | mixed |  |  | 5 | 53 | 5860 |
| autoPinLivePortfolioStrategies | engine |  |  |  | 9 | 2496 |
| capturePortfolioScenario | engine |  |  |  | 11 | 3674 |
| createSimilarPortfolio | mixed | yes |  | 3 | 25 | 4582 |
| currentPortfolioViewConfig | engine |  |  |  | 23 | 2358 |
| getMergedPortfolioModels | engine |  |  |  | 9 | 3904 |
| markPortfolioFixed | engine |  |  |  | 12 | 3686 |
| moveModelBetweenPortfolios | mixed | yes |  | 1 | 22 | 3881 |
| movePortfolio | engine |  |  |  | 13 | 2274 |
| pauseReplay | mixed |  |  | 4 | 11 | 6504 |
| persistPortfolioViewConfig | engine |  |  |  | 9 | 2382 |
| refreshActivePortfolioView | mixed | yes |  | 1 | 19 | 4147 |
| refreshLiveData | mixed | yes |  | 2 | 115 | 4779 |
| refreshPointInTimeSelection | mixed | yes | 1 | 11 | 211 | 6049 |
| removeModelFromPortfolio | engine | yes |  |  | 15 | 3711 |
| removePortfolios | engine | yes |  |  | 26 | 3742 |
| repopulateActivePortfolioFromCriteria | engine | yes |  |  | 14 | 4180 |
| resetAutomaticRankSchedule | mixed |  |  | 1 | 22 | 2045 |
| setRankingCriteria | mixed | yes |  | 5 | 146 | 5205 |
| startReplay | mixed |  |  | 4 | 13 | 6490 |
| switchDate | mixed | yes |  | 2 | 89 | 6324 |
| syncPortfolioViewRefresh | engine |  |  |  | 8 | 4167 |
| triggerSelectedTimeRefresh | mixed |  |  | 1 | 9 | 1968 |
| uniquePortfolioName | engine |  |  |  | 7 | 4574 |
| updateAutoRefreshTop1Status | view |  |  | 1 | 6 | 2009 |

## Engine call (rule logic removed from page) (12)

| Function | Kind | Async | Fetches | DOM refs | Lines | Line |
|---|---|---|---|---|---|---|
| applyAssignedOverlayTradeResults | engine |  |  |  | 67 | 2887 |
| asOfCorrelation | engine |  |  |  | 16 | 2790 |
| assignedRuleTarget | engine |  |  |  | 19 | 2955 |
| computeLeaderRotation | engine |  |  |  | 159 | 8149 |
| computeMultiSplitRotation | engine |  |  |  | 176 | 8312 |
| computeSplitTargetSignal | engine |  |  |  | 38 | 8047 |
| computeTradeOverlaySignals | engine |  |  |  | 143 | 7863 |
| curvePointAtOrBefore | engine |  |  |  | 11 | 2849 |
| overlayRuleCandidate | engine |  |  |  | 106 | 2683 |
| overlayRuleMetricValue | engine |  |  |  | 20 | 2572 |
| pairOverlayTrades | engine |  |  |  | 35 | 8009 |
| sourceTradeFlipResults | engine |  |  |  | 25 | 2861 |

## Ported in engine/page.py, NOT delegated (11)

| Function | Kind | Async | Fetches | DOM refs | Lines | Line |
|---|---|---|---|---|---|---|
| activePortfolioOverlayRule | engine |  |  |  | 4 | 2531 |
| assignedPortfolioOverlayRule | engine |  |  |  | 5 | 2525 |
| deletePortfolio | mixed | yes |  | 1 | 4 | 3727 |
| deleteSelectedPortfolios | mixed | yes |  | 1 | 9 | 3732 |
| livePortfolioModelsForDate | engine |  |  |  | 31 | 2464 |
| loadPortfolioData | engine | yes |  |  | 40 | 4043 |
| loadModelSearchFromDatabase | mixed | yes | 2 | 7 | 102 | 5622 |
| loadDeepLinkModelsFromDatabase | mixed | yes | 1 | 4 | 46 | 5725 |
| schedulePointInTimeSelection | mixed |  |  | 1 | 26 | 6260 |
| refreshPointInTimeHistory | mixed | yes | 1 | 4 | 26 | 6022 |
| scheduleAutomaticTop1Refresh | mixed |  |  | 2 | 47 | 5939 |

## Stays in page (34)

| Function | Kind | Async | Fetches | DOM refs | Lines | Line |
|---|---|---|---|---|---|---|
| activateLiveModeFromReview | mixed | yes | 1 | 38 | 93 | 3294 |
| appendRuleDetailsSection | mixed |  |  | 18 | 30 | 3495 |
| applyDisplayTheme | mixed |  |  | 9 | 11 | 3699 |
| assignOverlayRule | mixed | yes | 1 | 8 | 24 | 3055 |
| beginEditNamedOverlayRule | mixed |  |  | 33 | 28 | 2646 |
| cancelEditNamedOverlayRule | mixed |  |  | 9 | 7 | 2675 |
| configFromOverlayEditor | mixed |  |  | 16 | 16 | 2981 |
| editLivePortfolioRules | mixed | yes |  | 9 | 8 | 3579 |
| getEligibleModels | mixed |  |  | 9 | 71 | 5540 |
| loadHourlyReport | mixed | yes | 1 | 15 | 36 | 6736 |
| loadLivePortfolioRulesIntoForm | mixed | yes |  | 19 | 29 | 3439 |
| loadStrategyCatalogue | mixed | yes | 1 | 2 | 19 | 3851 |
| populateCataloguePortfolioOptions | mixed |  |  | 6 | 9 | 3779 |
| restorePortfolioWorkspaceFromPostgres | mixed | yes | 1 | 1 | 26 | 2331 |
| saveLivePortfolioRules | mixed | yes | 1 | 24 | 45 | 3624 |
| saveNamedOverlayRule | mixed | yes |  | 21 | 40 | 3014 |
| savePortfolioWorkspaceToPostgres | mixed | yes | 1 | 3 | 29 | 2301 |
| scheduleDashboardUtilityRuntime | mixed |  |  | 1 | 9 | 8991 |
| setAllSectionsCollapsed | mixed |  |  | 3 | 8 | 5134 |
| setCatalogueOptions | mixed |  |  | 9 | 9 | 3769 |
| setLiveBadge | mixed |  |  | 3 | 11 | 4767 |
| setSectionCollapsed | mixed |  |  | 7 | 8 | 5108 |
| setupCanvas | mixed |  |  | 2 | 13 | 7832 |
| setupCollapsibleSections | mixed |  |  | 9 | 23 | 5143 |
| setupDateTabs | mixed |  |  | 4 | 16 | 5185 |
| setupEventListeners | mixed |  |  | 160 | 648 | 6919 |
| setupTradesModal | mixed |  |  | 23 | 18 | 5088 |
| syncHourlyProducts | mixed |  |  | 3 | 6 | 6729 |
| syncLivePortfolioScreenState | mixed | yes |  | 1 | 35 | 3588 |
| syncSplitModeControls | mixed |  |  | 7 | 19 | 5449 |
| updateCollapseAllControl | mixed |  |  | 12 | 11 | 5122 |
| updateOverlayTradeSummary | mixed |  |  | 9 | 27 | 8539 |
| updateRibbon | mixed |  |  | 24 | 86 | 7591 |
| updateStrategyFamilyOptions | mixed |  |  | 1 | 4 | 5493 |
