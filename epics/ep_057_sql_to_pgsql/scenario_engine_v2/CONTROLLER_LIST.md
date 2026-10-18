# Controller list - page v2.65.32 (generated 2026-10-18 from inventory_v2.65.32/inventory.json, tools/controller_wrappers.py, engine/page.py)

A controller here = a page function that is not pure logic: kind `mixed` (state + DOM), plus the delegated or ported ones. Columns: kind, async, number of fetch endpoints, DOM references, lines, page start line.


## Delegated to engine (wrapper) (19)

| Function | Kind | Async | Fetches | DOM refs | Lines | Line |
|---|---|---|---|---|---|---|
| applyChartLock | mixed |  |  | 5 | 29 | 6687 |
| applyPortfolioViewConfig | mixed |  |  | 17 | 60 | 2332 |
| applySelectedTime | mixed |  |  | 5 | 53 | 5739 |
| autoPinLivePortfolioStrategies | engine |  |  |  | 9 | 2436 |
| capturePortfolioScenario | engine |  |  |  | 11 | 3614 |
| currentPortfolioViewConfig | engine |  |  |  | 23 | 2298 |
| getMergedPortfolioModels | engine |  |  |  | 9 | 3844 |
| markPortfolioFixed | engine |  |  |  | 12 | 3626 |
| movePortfolio | engine |  |  |  | 13 | 2214 |
| pauseReplay | mixed |  |  | 4 | 11 | 6383 |
| persistPortfolioViewConfig | engine |  |  |  | 9 | 2322 |
| resetAutomaticRankSchedule | mixed |  |  | 1 | 22 | 1985 |
| scheduleAutomaticTop1Refresh | mixed |  |  | 2 | 47 | 5818 |
| schedulePointInTimeSelection | mixed |  |  | 1 | 26 | 6139 |
| startReplay | mixed |  |  | 4 | 13 | 6369 |
| syncPortfolioViewRefresh | engine |  |  |  | 8 | 4107 |
| triggerSelectedTimeRefresh | mixed |  |  | 1 | 9 | 1908 |
| uniquePortfolioName | engine |  |  |  | 7 | 4511 |
| updateAutoRefreshTop1Status | view |  |  | 1 | 6 | 1949 |

## Engine call (rule logic removed from page) (12)

| Function | Kind | Async | Fetches | DOM refs | Lines | Line |
|---|---|---|---|---|---|---|
| applyAssignedOverlayTradeResults | engine |  |  |  | 67 | 2827 |
| asOfCorrelation | engine |  |  |  | 16 | 2730 |
| assignedRuleTarget | engine |  |  |  | 19 | 2895 |
| computeLeaderRotation | engine |  |  |  | 159 | 7894 |
| computeMultiSplitRotation | engine |  |  |  | 176 | 8057 |
| computeSplitTargetSignal | engine |  |  |  | 38 | 7825 |
| computeTradeOverlaySignals | engine |  |  |  | 143 | 7641 |
| curvePointAtOrBefore | engine |  |  |  | 11 | 2789 |
| overlayRuleCandidate | engine |  |  |  | 106 | 2623 |
| overlayRuleMetricValue | engine |  |  |  | 20 | 2512 |
| pairOverlayTrades | engine |  |  |  | 35 | 7787 |
| sourceTradeFlipResults | engine |  |  |  | 25 | 2801 |

## Ported in engine/page.py, NOT delegated (19)

| Function | Kind | Async | Fetches | DOM refs | Lines | Line |
|---|---|---|---|---|---|---|
| activatePortfolio | mixed | yes |  | 2 | 174 | 4135 |
| activePortfolioOverlayRule | engine |  |  |  | 4 | 2471 |
| addCatalogueModel | mixed | yes |  | 1 | 21 | 3729 |
| assignedPortfolioOverlayRule | engine |  |  |  | 5 | 2465 |
| createSimilarPortfolio | mixed | yes |  | 3 | 25 | 4519 |
| deletePortfolio | mixed | yes |  | 1 | 4 | 3667 |
| deleteSelectedPortfolios | mixed | yes |  | 1 | 9 | 3672 |
| livePortfolioModelsForDate | engine |  |  |  | 31 | 2404 |
| loadPortfolioData | engine | yes |  |  | 40 | 3983 |
| moveModelBetweenPortfolios | mixed | yes |  | 1 | 22 | 3821 |
| refreshActivePortfolioView | mixed | yes |  | 1 | 19 | 4087 |
| refreshLiveData | mixed | yes |  | 2 | 115 | 4716 |
| refreshPointInTimeHistory | mixed | yes | 1 | 4 | 26 | 5901 |
| refreshPointInTimeSelection | mixed | yes | 1 | 11 | 211 | 5928 |
| removeModelFromPortfolio | engine | yes |  |  | 15 | 3651 |
| removePortfolios | engine | yes |  |  | 26 | 3682 |
| repopulateActivePortfolioFromCriteria | engine | yes |  |  | 14 | 4120 |
| setRankingCriteria | mixed | yes |  | 5 | 146 | 5142 |
| switchDate | mixed | yes |  | 2 | 89 | 6203 |

## Stays in page (36)

| Function | Kind | Async | Fetches | DOM refs | Lines | Line |
|---|---|---|---|---|---|---|
| activateLiveModeFromReview | mixed | yes | 1 | 38 | 93 | 3234 |
| appendRuleDetailsSection | mixed |  |  | 18 | 30 | 3435 |
| applyDisplayTheme | mixed |  |  | 9 | 11 | 3639 |
| assignOverlayRule | mixed | yes | 1 | 8 | 24 | 2995 |
| beginEditNamedOverlayRule | mixed |  |  | 33 | 28 | 2586 |
| cancelEditNamedOverlayRule | mixed |  |  | 9 | 7 | 2615 |
| configFromOverlayEditor | mixed |  |  | 16 | 16 | 2921 |
| editLivePortfolioRules | mixed | yes |  | 9 | 8 | 3519 |
| getEligibleModels | mixed |  |  | 8 | 62 | 5473 |
| loadDeepLinkModelsFromDatabase | mixed | yes | 1 | 4 | 46 | 5604 |
| loadHourlyReport | mixed | yes | 1 | 15 | 36 | 6615 |
| loadLivePortfolioRulesIntoForm | mixed | yes |  | 19 | 29 | 3379 |
| loadModelSearchFromDatabase | mixed | yes | 1 | 6 | 57 | 5546 |
| loadStrategyCatalogue | mixed | yes | 1 | 2 | 19 | 3791 |
| populateCataloguePortfolioOptions | mixed |  |  | 6 | 9 | 3719 |
| restorePortfolioWorkspaceFromPostgres | mixed | yes | 1 | 1 | 26 | 2271 |
| saveLivePortfolioRules | mixed | yes | 1 | 24 | 45 | 3564 |
| saveNamedOverlayRule | mixed | yes |  | 21 | 40 | 2954 |
| savePortfolioWorkspaceToPostgres | mixed | yes | 1 | 3 | 29 | 2241 |
| scheduleDashboardUtilityRuntime | mixed |  |  | 1 | 9 | 8727 |
| setAllSectionsCollapsed | mixed |  |  | 3 | 8 | 5071 |
| setCatalogueOptions | mixed |  |  | 9 | 9 | 3709 |
| setLiveBadge | mixed |  |  | 3 | 11 | 4704 |
| setSectionCollapsed | mixed |  |  | 7 | 8 | 5045 |
| setupCanvas | mixed |  |  | 2 | 13 | 7610 |
| setupCollapsibleSections | mixed |  |  | 9 | 23 | 5080 |
| setupDateTabs | mixed |  |  | 4 | 16 | 5122 |
| setupEventListeners | mixed |  |  | 150 | 632 | 6717 |
| setupTradesModal | mixed |  |  | 23 | 18 | 5025 |
| syncHourlyProducts | mixed |  |  | 3 | 6 | 6608 |
| syncLivePortfolioScreenState | mixed | yes |  | 1 | 35 | 3528 |
| syncSplitModeControls | mixed |  |  | 7 | 19 | 5382 |
| updateCollapseAllControl | mixed |  |  | 12 | 11 | 5059 |
| updateOverlayTradeSummary | mixed |  |  | 9 | 27 | 8284 |
| updateRibbon | mixed |  |  | 24 | 86 | 7373 |
| updateStrategyFamilyOptions | mixed |  |  | 1 | 4 | 5426 |
