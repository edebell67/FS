# Controller list - page v2.65.56 (generated 2026-10-22 from inventory_v2.65.56/inventory.json, tools/controller_wrappers.py, engine/page.py)

A controller here = a page function that is not pure logic: kind `mixed` (state + DOM), plus the delegated or ported ones. Columns: kind, async, number of fetch endpoints, DOM references, lines, page start line.


## Delegated to engine (wrapper) (29)

| Function | Kind | Async | Fetches | DOM refs | Lines | Line |
|---|---|---|---|---|---|---|
| activatePortfolio | mixed | yes |  | 2 | 180 | 4274 |
| addCatalogueModel | mixed | yes |  | 1 | 21 | 3860 |
| applyChartLock | mixed |  |  | 5 | 29 | 7299 |
| applyPortfolioViewConfig | mixed |  |  | 17 | 60 | 2461 |
| applySelectedTime | mixed |  |  | 3 | 49 | 6177 |
| autoPinLivePortfolioStrategies | engine |  |  |  | 9 | 2565 |
| capturePortfolioScenario | engine |  |  |  | 11 | 3745 |
| createSimilarPortfolio | mixed | yes |  | 3 | 25 | 4664 |
| currentPortfolioViewConfig | engine |  |  |  | 23 | 2427 |
| getMergedPortfolioModels | engine |  |  |  | 9 | 3975 |
| markPortfolioFixed | engine |  |  |  | 12 | 3757 |
| moveModelBetweenPortfolios | mixed | yes |  | 1 | 22 | 3952 |
| movePortfolio | engine |  |  |  | 13 | 2343 |
| pauseReplay | mixed |  |  | 4 | 11 | 6817 |
| persistPortfolioViewConfig | engine |  |  |  | 9 | 2451 |
| refreshActivePortfolioView | mixed | yes |  | 1 | 19 | 4219 |
| refreshLiveData | mixed | yes |  | 2 | 117 | 4859 |
| refreshPointInTimeSelection | mixed | yes | 1 | 11 | 211 | 6362 |
| removeModelFromPortfolio | engine | yes |  |  | 15 | 3782 |
| removePortfolios | engine | yes |  |  | 26 | 3813 |
| repopulateActivePortfolioFromCriteria | engine | yes |  |  | 14 | 4259 |
| resetAutomaticRankSchedule | mixed |  |  | 1 | 22 | 2096 |
| setRankingCriteria | mixed | yes |  | 5 | 146 | 5287 |
| startReplay | mixed |  |  | 4 | 13 | 6803 |
| switchDate | mixed | yes |  | 2 | 89 | 6637 |
| syncPortfolioViewRefresh | engine |  |  |  | 8 | 4239 |
| triggerSelectedTimeRefresh | mixed |  |  | 1 | 9 | 2011 |
| uniquePortfolioName | engine |  |  |  | 7 | 4656 |
| updateAutoRefreshTop1Status | view |  |  | 1 | 6 | 2060 |

## Engine call (rule logic removed from page) (12)

| Function | Kind | Async | Fetches | DOM refs | Lines | Line |
|---|---|---|---|---|---|---|
| applyAssignedOverlayTradeResults | engine |  |  |  | 67 | 2956 |
| asOfCorrelation | engine |  |  |  | 16 | 2859 |
| assignedRuleTarget | engine |  |  |  | 19 | 3024 |
| computeLeaderRotation | engine |  |  |  | 159 | 8634 |
| computeMultiSplitRotation | engine |  |  |  | 176 | 8797 |
| computeSplitTargetSignal | engine |  |  |  | 38 | 8528 |
| computeTradeOverlaySignals | engine |  |  |  | 143 | 8344 |
| curvePointAtOrBefore | engine |  |  |  | 11 | 2918 |
| overlayRuleCandidate | engine |  |  |  | 106 | 2752 |
| overlayRuleMetricValue | engine |  |  |  | 20 | 2641 |
| pairOverlayTrades | engine |  |  |  | 35 | 8490 |
| sourceTradeFlipResults | engine |  |  |  | 25 | 2930 |

## Ported in engine/page.py, NOT delegated (11)

| Function | Kind | Async | Fetches | DOM refs | Lines | Line |
|---|---|---|---|---|---|---|
| activePortfolioOverlayRule | engine |  |  |  | 4 | 2600 |
| assignedPortfolioOverlayRule | engine |  |  |  | 5 | 2594 |
| deletePortfolio | mixed | yes |  | 1 | 4 | 3798 |
| deleteSelectedPortfolios | mixed | yes |  | 1 | 9 | 3803 |
| livePortfolioModelsForDate | engine |  |  |  | 31 | 2533 |
| loadPortfolioData | engine | yes |  |  | 40 | 4115 |
| loadModelSearchFromDatabase | mixed | yes | 5 | 13 | 193 | 5804 |
| loadDeepLinkModelsFromDatabase | mixed | yes |  | 4 | 75 | 5998 |
| schedulePointInTimeSelection | mixed |  |  | 1 | 26 | 6573 |
| refreshPointInTimeHistory | mixed | yes | 1 | 4 | 26 | 6335 |
| scheduleAutomaticTop1Refresh | mixed |  |  | 2 | 47 | 6252 |

## Stays in page (34)

| Function | Kind | Async | Fetches | DOM refs | Lines | Line |
|---|---|---|---|---|---|---|
| activateLiveModeFromReview | mixed | yes | 1 | 38 | 93 | 3365 |
| appendRuleDetailsSection | mixed |  |  | 18 | 30 | 3566 |
| applyDisplayTheme | mixed |  |  | 9 | 11 | 3770 |
| assignOverlayRule | mixed | yes | 1 | 8 | 24 | 3124 |
| beginEditNamedOverlayRule | mixed |  |  | 33 | 28 | 2715 |
| cancelEditNamedOverlayRule | mixed |  |  | 9 | 7 | 2744 |
| configFromOverlayEditor | mixed |  |  | 16 | 16 | 3050 |
| editLivePortfolioRules | mixed | yes |  | 9 | 8 | 3650 |
| getEligibleModels | mixed |  |  | 10 | 90 | 5637 |
| loadHourlyReport | mixed | yes | 1 | 15 | 36 | 7049 |
| loadLivePortfolioRulesIntoForm | mixed | yes |  | 19 | 29 | 3510 |
| loadStrategyCatalogue | mixed | yes | 1 | 2 | 19 | 3922 |
| populateCataloguePortfolioOptions | mixed |  |  | 6 | 9 | 3850 |
| restorePortfolioWorkspaceFromPostgres | mixed | yes | 1 | 1 | 26 | 2400 |
| saveLivePortfolioRules | mixed | yes | 1 | 24 | 45 | 3695 |
| saveNamedOverlayRule | mixed | yes |  | 21 | 40 | 3083 |
| savePortfolioWorkspaceToPostgres | mixed | yes | 1 | 3 | 29 | 2370 |
| scheduleDashboardUtilityRuntime | mixed |  |  | 1 | 9 | 9476 |
| setAllSectionsCollapsed | mixed |  |  | 3 | 8 | 5216 |
| setCatalogueOptions | mixed |  |  | 9 | 9 | 3840 |
| setLiveBadge | mixed |  |  | 3 | 11 | 4847 |
| setSectionCollapsed | mixed |  |  | 7 | 8 | 5190 |
| setupCanvas | mixed |  |  | 2 | 13 | 8313 |
| setupCollapsibleSections | mixed |  |  | 9 | 23 | 5225 |
| setupDateTabs | mixed |  |  | 4 | 16 | 5267 |
| setupEventListeners | mixed |  |  | 161 | 706 | 7329 |
| setupTradesModal | mixed |  |  | 23 | 18 | 5170 |
| syncHourlyProducts | mixed |  |  | 3 | 6 | 7042 |
| syncLivePortfolioScreenState | mixed | yes |  | 1 | 35 | 3659 |
| syncSplitModeControls | mixed |  |  | 7 | 19 | 5532 |
| updateCollapseAllControl | mixed |  |  | 12 | 11 | 5204 |
| updateOverlayTradeSummary | mixed |  |  | 9 | 27 | 9024 |
| updateRibbon | mixed |  |  | 24 | 86 | 8059 |
| updateStrategyFamilyOptions | mixed |  |  | 1 | 4 | 5576 |
