# Controller list - page v2.65.35 (generated 2026-10-19 from inventory_v2.65.35/inventory.json, tools/controller_wrappers.py, engine/page.py)

A controller here = a page function that is not pure logic: kind `mixed` (state + DOM), plus the delegated or ported ones. Columns: kind, async, number of fetch endpoints, DOM references, lines, page start line.


## Delegated to engine (wrapper) (31)

| Function | Kind | Async | Fetches | DOM refs | Lines | Line |
|---|---|---|---|---|---|---|
| activatePortfolio | mixed | yes |  | 2 | 177 | 4138 |
| addCatalogueModel | mixed | yes |  | 1 | 21 | 3732 |
| applyChartLock | mixed |  |  | 5 | 29 | 6721 |
| applyPortfolioViewConfig | mixed |  |  | 17 | 60 | 2335 |
| applySelectedTime | mixed |  |  | 5 | 53 | 5773 |
| autoPinLivePortfolioStrategies | engine |  |  |  | 9 | 2439 |
| capturePortfolioScenario | engine |  |  |  | 11 | 3617 |
| createSimilarPortfolio | mixed | yes |  | 3 | 25 | 4525 |
| currentPortfolioViewConfig | engine |  |  |  | 23 | 2301 |
| getMergedPortfolioModels | engine |  |  |  | 9 | 3847 |
| markPortfolioFixed | engine |  |  |  | 12 | 3629 |
| moveModelBetweenPortfolios | mixed | yes |  | 1 | 22 | 3824 |
| movePortfolio | engine |  |  |  | 13 | 2217 |
| pauseReplay | mixed |  |  | 4 | 11 | 6417 |
| persistPortfolioViewConfig | engine |  |  |  | 9 | 2325 |
| refreshActivePortfolioView | mixed | yes |  | 1 | 19 | 4090 |
| refreshLiveData | mixed | yes |  | 2 | 115 | 4722 |
| refreshPointInTimeHistory | mixed | yes | 1 | 4 | 26 | 5935 |
| refreshPointInTimeSelection | mixed | yes | 1 | 11 | 211 | 5962 |
| removeModelFromPortfolio | engine | yes |  |  | 15 | 3654 |
| removePortfolios | engine | yes |  |  | 26 | 3685 |
| repopulateActivePortfolioFromCriteria | engine | yes |  |  | 14 | 4123 |
| resetAutomaticRankSchedule | mixed |  |  | 1 | 22 | 1988 |
| scheduleAutomaticTop1Refresh | mixed |  |  | 2 | 47 | 5852 |
| setRankingCriteria | mixed | yes |  | 5 | 146 | 5148 |
| startReplay | mixed |  |  | 4 | 13 | 6403 |
| switchDate | mixed | yes |  | 2 | 89 | 6237 |
| syncPortfolioViewRefresh | engine |  |  |  | 8 | 4110 |
| triggerSelectedTimeRefresh | mixed |  |  | 1 | 9 | 1911 |
| uniquePortfolioName | engine |  |  |  | 7 | 4517 |
| updateAutoRefreshTop1Status | view |  |  | 1 | 6 | 1952 |

## Engine call (rule logic removed from page) (12)

| Function | Kind | Async | Fetches | DOM refs | Lines | Line |
|---|---|---|---|---|---|---|
| applyAssignedOverlayTradeResults | engine |  |  |  | 67 | 2830 |
| asOfCorrelation | engine |  |  |  | 16 | 2733 |
| assignedRuleTarget | engine |  |  |  | 19 | 2898 |
| computeLeaderRotation | engine |  |  |  | 159 | 7928 |
| computeMultiSplitRotation | engine |  |  |  | 176 | 8091 |
| computeSplitTargetSignal | engine |  |  |  | 38 | 7859 |
| computeTradeOverlaySignals | engine |  |  |  | 143 | 7675 |
| curvePointAtOrBefore | engine |  |  |  | 11 | 2792 |
| overlayRuleCandidate | engine |  |  |  | 106 | 2626 |
| overlayRuleMetricValue | engine |  |  |  | 20 | 2515 |
| pairOverlayTrades | engine |  |  |  | 35 | 7821 |
| sourceTradeFlipResults | engine |  |  |  | 25 | 2804 |

## Ported in engine/page.py, NOT delegated (9)

| Function | Kind | Async | Fetches | DOM refs | Lines | Line |
|---|---|---|---|---|---|---|
| activePortfolioOverlayRule | engine |  |  |  | 4 | 2474 |
| assignedPortfolioOverlayRule | engine |  |  |  | 5 | 2468 |
| deletePortfolio | mixed | yes |  | 1 | 4 | 3670 |
| deleteSelectedPortfolios | mixed | yes |  | 1 | 9 | 3675 |
| livePortfolioModelsForDate | engine |  |  |  | 31 | 2407 |
| loadPortfolioData | engine | yes |  |  | 40 | 3986 |
| loadModelSearchFromDatabase | mixed | yes | 2 | 7 | 86 | 5551 |
| loadDeepLinkModelsFromDatabase | mixed | yes | 1 | 4 | 46 | 5638 |
| schedulePointInTimeSelection | mixed |  |  | 1 | 26 | 6173 |

## Stays in page (34)

| Function | Kind | Async | Fetches | DOM refs | Lines | Line |
|---|---|---|---|---|---|---|
| activateLiveModeFromReview | mixed | yes | 1 | 38 | 93 | 3237 |
| appendRuleDetailsSection | mixed |  |  | 18 | 30 | 3438 |
| applyDisplayTheme | mixed |  |  | 9 | 11 | 3642 |
| assignOverlayRule | mixed | yes | 1 | 8 | 24 | 2998 |
| beginEditNamedOverlayRule | mixed |  |  | 33 | 28 | 2589 |
| cancelEditNamedOverlayRule | mixed |  |  | 9 | 7 | 2618 |
| configFromOverlayEditor | mixed |  |  | 16 | 16 | 2924 |
| editLivePortfolioRules | mixed | yes |  | 9 | 8 | 3522 |
| getEligibleModels | mixed |  |  | 8 | 61 | 5479 |
| loadHourlyReport | mixed | yes | 1 | 15 | 36 | 6649 |
| loadLivePortfolioRulesIntoForm | mixed | yes |  | 19 | 29 | 3382 |
| loadStrategyCatalogue | mixed | yes | 1 | 2 | 19 | 3794 |
| populateCataloguePortfolioOptions | mixed |  |  | 6 | 9 | 3722 |
| restorePortfolioWorkspaceFromPostgres | mixed | yes | 1 | 1 | 26 | 2274 |
| saveLivePortfolioRules | mixed | yes | 1 | 24 | 45 | 3567 |
| saveNamedOverlayRule | mixed | yes |  | 21 | 40 | 2957 |
| savePortfolioWorkspaceToPostgres | mixed | yes | 1 | 3 | 29 | 2244 |
| scheduleDashboardUtilityRuntime | mixed |  |  | 1 | 9 | 8761 |
| setAllSectionsCollapsed | mixed |  |  | 3 | 8 | 5077 |
| setCatalogueOptions | mixed |  |  | 9 | 9 | 3712 |
| setLiveBadge | mixed |  |  | 3 | 11 | 4710 |
| setSectionCollapsed | mixed |  |  | 7 | 8 | 5051 |
| setupCanvas | mixed |  |  | 2 | 13 | 7644 |
| setupCollapsibleSections | mixed |  |  | 9 | 23 | 5086 |
| setupDateTabs | mixed |  |  | 4 | 16 | 5128 |
| setupEventListeners | mixed |  |  | 150 | 632 | 6751 |
| setupTradesModal | mixed |  |  | 23 | 18 | 5031 |
| syncHourlyProducts | mixed |  |  | 3 | 6 | 6642 |
| syncLivePortfolioScreenState | mixed | yes |  | 1 | 35 | 3531 |
| syncSplitModeControls | mixed |  |  | 7 | 19 | 5388 |
| updateCollapseAllControl | mixed |  |  | 12 | 11 | 5065 |
| updateOverlayTradeSummary | mixed |  |  | 9 | 27 | 8318 |
| updateRibbon | mixed |  |  | 24 | 86 | 7407 |
| updateStrategyFamilyOptions | mixed |  |  | 1 | 4 | 5432 |
