# Controller list - page v2.65.55 (generated 2026-10-22 from inventory_v2.65.55/inventory.json, tools/controller_wrappers.py, engine/page.py)

A controller here = a page function that is not pure logic: kind `mixed` (state + DOM), plus the delegated or ported ones. Columns: kind, async, number of fetch endpoints, DOM references, lines, page start line.


## Delegated to engine (wrapper) (29)

| Function | Kind | Async | Fetches | DOM refs | Lines | Line |
|---|---|---|---|---|---|---|
| activatePortfolio | mixed | yes |  | 2 | 180 | 4267 |
| addCatalogueModel | mixed | yes |  | 1 | 21 | 3853 |
| applyChartLock | mixed |  |  | 5 | 29 | 7240 |
| applyPortfolioViewConfig | mixed |  |  | 17 | 60 | 2454 |
| applySelectedTime | mixed |  |  | 3 | 49 | 6170 |
| autoPinLivePortfolioStrategies | engine |  |  |  | 9 | 2558 |
| capturePortfolioScenario | engine |  |  |  | 11 | 3738 |
| createSimilarPortfolio | mixed | yes |  | 3 | 25 | 4657 |
| currentPortfolioViewConfig | engine |  |  |  | 23 | 2420 |
| getMergedPortfolioModels | engine |  |  |  | 9 | 3968 |
| markPortfolioFixed | engine |  |  |  | 12 | 3750 |
| moveModelBetweenPortfolios | mixed | yes |  | 1 | 22 | 3945 |
| movePortfolio | engine |  |  |  | 13 | 2336 |
| pauseReplay | mixed |  |  | 4 | 11 | 6810 |
| persistPortfolioViewConfig | engine |  |  |  | 9 | 2444 |
| refreshActivePortfolioView | mixed | yes |  | 1 | 19 | 4212 |
| refreshLiveData | mixed | yes |  | 2 | 117 | 4852 |
| refreshPointInTimeSelection | mixed | yes | 1 | 11 | 211 | 6355 |
| removeModelFromPortfolio | engine | yes |  |  | 15 | 3775 |
| removePortfolios | engine | yes |  |  | 26 | 3806 |
| repopulateActivePortfolioFromCriteria | engine | yes |  |  | 14 | 4252 |
| resetAutomaticRankSchedule | mixed |  |  | 1 | 22 | 2089 |
| setRankingCriteria | mixed | yes |  | 5 | 146 | 5280 |
| startReplay | mixed |  |  | 4 | 13 | 6796 |
| switchDate | mixed | yes |  | 2 | 89 | 6630 |
| syncPortfolioViewRefresh | engine |  |  |  | 8 | 4232 |
| triggerSelectedTimeRefresh | mixed |  |  | 1 | 9 | 2004 |
| uniquePortfolioName | engine |  |  |  | 7 | 4649 |
| updateAutoRefreshTop1Status | view |  |  | 1 | 6 | 2053 |

## Engine call (rule logic removed from page) (12)

| Function | Kind | Async | Fetches | DOM refs | Lines | Line |
|---|---|---|---|---|---|---|
| applyAssignedOverlayTradeResults | engine |  |  |  | 67 | 2949 |
| asOfCorrelation | engine |  |  |  | 16 | 2852 |
| assignedRuleTarget | engine |  |  |  | 19 | 3017 |
| computeLeaderRotation | engine |  |  |  | 159 | 8570 |
| computeMultiSplitRotation | engine |  |  |  | 176 | 8733 |
| computeSplitTargetSignal | engine |  |  |  | 38 | 8464 |
| computeTradeOverlaySignals | engine |  |  |  | 143 | 8280 |
| curvePointAtOrBefore | engine |  |  |  | 11 | 2911 |
| overlayRuleCandidate | engine |  |  |  | 106 | 2745 |
| overlayRuleMetricValue | engine |  |  |  | 20 | 2634 |
| pairOverlayTrades | engine |  |  |  | 35 | 8426 |
| sourceTradeFlipResults | engine |  |  |  | 25 | 2923 |

## Ported in engine/page.py, NOT delegated (11)

| Function | Kind | Async | Fetches | DOM refs | Lines | Line |
|---|---|---|---|---|---|---|
| activePortfolioOverlayRule | engine |  |  |  | 4 | 2593 |
| assignedPortfolioOverlayRule | engine |  |  |  | 5 | 2587 |
| deletePortfolio | mixed | yes |  | 1 | 4 | 3791 |
| deleteSelectedPortfolios | mixed | yes |  | 1 | 9 | 3796 |
| livePortfolioModelsForDate | engine |  |  |  | 31 | 2526 |
| loadPortfolioData | engine | yes |  |  | 40 | 4108 |
| loadModelSearchFromDatabase | mixed | yes | 5 | 13 | 193 | 5797 |
| loadDeepLinkModelsFromDatabase | mixed | yes |  | 4 | 75 | 5991 |
| schedulePointInTimeSelection | mixed |  |  | 1 | 26 | 6566 |
| refreshPointInTimeHistory | mixed | yes | 1 | 4 | 26 | 6328 |
| scheduleAutomaticTop1Refresh | mixed |  |  | 2 | 47 | 6245 |

## Stays in page (34)

| Function | Kind | Async | Fetches | DOM refs | Lines | Line |
|---|---|---|---|---|---|---|
| activateLiveModeFromReview | mixed | yes | 1 | 38 | 93 | 3358 |
| appendRuleDetailsSection | mixed |  |  | 18 | 30 | 3559 |
| applyDisplayTheme | mixed |  |  | 9 | 11 | 3763 |
| assignOverlayRule | mixed | yes | 1 | 8 | 24 | 3117 |
| beginEditNamedOverlayRule | mixed |  |  | 33 | 28 | 2708 |
| cancelEditNamedOverlayRule | mixed |  |  | 9 | 7 | 2737 |
| configFromOverlayEditor | mixed |  |  | 16 | 16 | 3043 |
| editLivePortfolioRules | mixed | yes |  | 9 | 8 | 3643 |
| getEligibleModels | mixed |  |  | 10 | 90 | 5630 |
| loadHourlyReport | mixed | yes | 1 | 15 | 36 | 7042 |
| loadLivePortfolioRulesIntoForm | mixed | yes |  | 19 | 29 | 3503 |
| loadStrategyCatalogue | mixed | yes | 1 | 2 | 19 | 3915 |
| populateCataloguePortfolioOptions | mixed |  |  | 6 | 9 | 3843 |
| restorePortfolioWorkspaceFromPostgres | mixed | yes | 1 | 1 | 26 | 2393 |
| saveLivePortfolioRules | mixed | yes | 1 | 24 | 45 | 3688 |
| saveNamedOverlayRule | mixed | yes |  | 21 | 40 | 3076 |
| savePortfolioWorkspaceToPostgres | mixed | yes | 1 | 3 | 29 | 2363 |
| scheduleDashboardUtilityRuntime | mixed |  |  | 1 | 9 | 9412 |
| setAllSectionsCollapsed | mixed |  |  | 3 | 8 | 5209 |
| setCatalogueOptions | mixed |  |  | 9 | 9 | 3833 |
| setLiveBadge | mixed |  |  | 3 | 11 | 4840 |
| setSectionCollapsed | mixed |  |  | 7 | 8 | 5183 |
| setupCanvas | mixed |  |  | 2 | 13 | 8249 |
| setupCollapsibleSections | mixed |  |  | 9 | 23 | 5218 |
| setupDateTabs | mixed |  |  | 4 | 16 | 5260 |
| setupEventListeners | mixed |  |  | 160 | 701 | 7270 |
| setupTradesModal | mixed |  |  | 23 | 18 | 5163 |
| syncHourlyProducts | mixed |  |  | 3 | 6 | 7035 |
| syncLivePortfolioScreenState | mixed | yes |  | 1 | 35 | 3652 |
| syncSplitModeControls | mixed |  |  | 7 | 19 | 5525 |
| updateCollapseAllControl | mixed |  |  | 12 | 11 | 5197 |
| updateOverlayTradeSummary | mixed |  |  | 9 | 27 | 8960 |
| updateRibbon | mixed |  |  | 24 | 86 | 7995 |
| updateStrategyFamilyOptions | mixed |  |  | 1 | 4 | 5569 |
