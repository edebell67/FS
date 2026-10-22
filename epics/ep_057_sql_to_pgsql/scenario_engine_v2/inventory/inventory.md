# Inventory of top10_5min_equity_curves (snapshot v2.65.24)

Source: `top10_5min_equity_curves_source_v2.65.24.html`; main script lines 1424-8975.

- functions: **205** (engine 110, view 38, mixed 57)
- top-level state variables: **272**
- top-level wiring statements: **5**

Classification is a heuristic: `engine` = no DOM references; `view` = DOM references and a render/UI-style name; `mixed` = DOM references and an unclear name, needing a manual split in the engine-core task.

| # | function | kind | lines | DOM refs | async | fetch | storage |
|---|---|---|---|---|---|---|---|
| 1 | `syncTpSlScenarios` | engine | 1497-1518 | 0 |  |  |  |
| 2 | `isMetricAwareCriteria` | engine | 1519-1528 | 0 |  |  |  |
| 3 | `liveChartCacheKey` | engine | 1536-1541 | 0 |  |  |  |
| 4 | `restoreLiveChartCache` | engine | 1542-1561 | 0 |  |  | y |
| 5 | `paintLiveChartCache` | engine | 1562-1570 | 0 |  |  |  |
| 6 | `scheduleLiveChartCacheFallback` | engine | 1571-1582 | 0 |  |  |  |
| 7 | `cacheLiveChartResponse` | engine | 1584-1615 | 0 |  |  | y |
| 8 | `ensureHistoricalDataLoaded` | engine | 1617-1635 | 0 | y |  |  |
| 9 | `availableDates` | engine | 1771-1782 | 0 |  |  |  |
| 10 | `triggerSelectedTimeRefresh` | mixed | 1896-1904 | 1 |  |  |  |
| 11 | `updateAutoRefreshTop1Status` | view | 1936-1941 | 1 |  |  |  |
| 12 | `finishAutomaticTop1Refresh` | engine | 1942-1959 | 0 |  |  |  |
| 13 | `resetAutomaticRankSchedule` | mixed | 1972-1993 | 1 |  |  |  |
| 14 | `setReturnType` | engine | 2077-2117 | 0 |  |  |  |
| 15 | `setReturnType` | engine | 2123-2186 | 0 |  |  | y |
| 16 | `syncLiveAltReporting` | engine | 2188-2194 | 0 |  |  |  |
| 17 | `savePortfolios` | engine | 2196-2199 | 0 |  |  | y |
| 18 | `movePortfolio` | engine | 2201-2213 | 0 |  |  |  |
| 19 | `saveCriteriaWorkspaces` | engine | 2215-2219 | 0 |  |  | y |
| 20 | `savePortfolioWorkspaceToPostgres` | mixed | 2228-2256 | 3 | y | ${API_BASE}/api/scenario_workspace | y |
| 21 | `restorePortfolioWorkspaceFromPostgres` | mixed | 2258-2283 | 1 | y | ${API_BASE}/api/scenario_workspace | y |
| 22 | `currentPortfolioViewConfig` | engine | 2285-2303 | 0 |  |  |  |
| 23 | `persistPortfolioViewConfig` | engine | 2305-2313 | 0 |  |  | y |
| 24 | `applyPortfolioViewConfig` | mixed | 2315-2369 | 14 |  |  |  |
| 25 | `loadLivePortfolioStore` | engine | 2371-2380 | 0 | y | ${location.origin}/api/live_portfolios |  |
| 26 | `livePortfolioModelsForDate` | engine | 2382-2412 | 0 |  |  |  |
| 27 | `autoPinLivePortfolioStrategies` | engine | 2414-2422 | 0 |  |  |  |
| 28 | `loadOverlayRuleLibrary` | engine | 2424-2441 | 0 | y | ${API_BASE}/api/overlay_rules |  |
| 29 | `assignedPortfolioOverlayRule` | engine | 2443-2447 | 0 |  |  |  |
| 30 | `activePortfolioOverlayRule` | engine | 2449-2452 | 0 |  |  |  |
| 31 | `syncAssignedOverlayRuleUI` | view | 2454-2473 | 9 |  |  |  |
| 32 | `overlayRuleSummary` | engine | 2475-2488 | 0 |  |  |  |
| 33 | `overlayRuleMetricValue` | engine | 2490-2509 | 0 |  |  |  |
| 34 | `renderOverlayRuleLibrary` | view | 2511-2562 | 40 |  |  |  |
| 35 | `beginEditNamedOverlayRule` | mixed | 2564-2591 | 33 |  |  |  |
| 36 | `cancelEditNamedOverlayRule` | mixed | 2593-2599 | 9 |  |  |  |
| 37 | `overlayRuleCandidate` | engine | 2601-2706 | 0 |  |  |  |
| 38 | `asOfCorrelation` | engine | 2708-2723 | 0 |  |  |  |
| 39 | `assignedOverlayTradeCacheKey` | engine | 2725-2727 | 0 |  |  |  |
| 40 | `ensureAssignedOverlayTradeData` | engine | 2729-2760 | 0 | y |  |  |
| 41 | `timeOfDayMinutes` | engine | 2762-2765 | 0 |  |  |  |
| 42 | `curvePointAtOrBefore` | engine | 2767-2777 | 0 |  |  |  |
| 43 | `sourceTradeFlipResults` | engine | 2779-2803 | 0 |  |  |  |
| 44 | `applyAssignedOverlayTradeResults` | engine | 2805-2871 | 0 |  |  |  |
| 45 | `assignedRuleTarget` | engine | 2873-2891 | 0 |  |  |  |
| 46 | `openOverlayRuleLibrary` | view | 2893-2897 | 1 | y |  |  |
| 47 | `configFromOverlayEditor` | mixed | 2899-2914 | 16 |  |  |  |
| 48 | `openNamedOverlayRuleSave` | view | 2916-2930 | 17 |  |  |  |
| 49 | `saveNamedOverlayRule` | mixed | 2932-2971 | 21 | y |  |  |
| 50 | `assignOverlayRule` | mixed | 2973-2996 | 8 | y | ${API_BASE}/api/overlay_rules/assignments/${encodeURICompone |  |
| 51 | `renderLivePortfolioTransition` | view | 2998-3024 | 3 |  |  |  |
| 52 | `isLiveModePortfolio` | engine | 3026-3028 | 0 |  |  |  |
| 53 | `isLiveModeArmed` | engine | 3030-3033 | 0 |  |  |  |
| 54 | `syncStrategyRemovalButtons` | view | 3035-3054 | 4 |  |  |  |
| 55 | `syncLiveModeUI` | view | 3056-3113 | 12 |  |  |  |
| 56 | `liveActivationRulesReady` | engine | 3119-3126 | 0 |  |  |  |
| 57 | `liveActivationRuleLabel` | engine | 3128-3142 | 0 |  |  |  |
| 58 | `syncLiveActivationReview` | view | 3144-3184 | 44 |  |  |  |
| 59 | `showLiveActivationReview` | view | 3186-3210 | 27 | y |  |  |
| 60 | `activateLiveModeFromReview` | mixed | 3212-3304 | 38 | y | ${location.origin}/api/live_portfolios/config |  |
| 61 | `toggleLiveMode` | view | 3306-3355 | 3 | y | ${location.origin}/api/live_portfolios/config |  |
| 62 | `loadLivePortfolioRulesIntoForm` | mixed | 3357-3385 | 19 | y |  |  |
| 63 | `isRuleManagedLivePortfolio` | engine | 3387-3389 | 0 |  |  |  |
| 64 | `liveRuleSummary` | engine | 3391-3411 | 0 |  |  |  |
| 65 | `appendRuleDetailsSection` | mixed | 3413-3442 | 18 |  |  |  |
| 66 | `showLivePortfolioRuleDetails` | view | 3444-3495 | 12 | y |  |  |
| 67 | `editLivePortfolioRules` | mixed | 3497-3504 | 9 | y |  |  |
| 68 | `syncLivePortfolioScreenState` | mixed | 3506-3540 | 1 | y |  |  |
| 69 | `saveLivePortfolioRules` | mixed | 3542-3586 | 24 | y | ${location.origin}/api/live_portfolios/config |  |
| 70 | `portfolioScenarioConfig` | engine | 3588-3590 | 0 |  |  |  |
| 71 | `capturePortfolioScenario` | engine | 3592-3602 | 0 |  |  | y |
| 72 | `markPortfolioFixed` | engine | 3604-3615 | 0 |  |  |  |
| 73 | `applyDisplayTheme` | mixed | 3617-3627 | 9 |  |  | y |
| 74 | `removeModelFromPortfolio` | engine | 3629-3643 | 0 | y |  |  |
| 75 | `deletePortfolio` | mixed | 3645-3648 | 1 | y |  |  |
| 76 | `deleteSelectedPortfolios` | mixed | 3650-3658 | 1 | y |  |  |
| 77 | `removePortfolios` | engine | 3660-3685 | 0 | y |  | y |
| 78 | `setCatalogueOptions` | mixed | 3687-3695 | 9 |  |  |  |
| 79 | `populateCataloguePortfolioOptions` | mixed | 3697-3705 | 6 |  |  |  |
| 80 | `addCatalogueModel` | mixed | 3707-3727 | 1 | y |  |  |
| 81 | `renderStrategyCatalogue` | view | 3729-3767 | 17 |  |  |  |
| 82 | `loadStrategyCatalogue` | mixed | 3769-3787 | 2 | y | ${API_BASE}/api/strategy_catalog?date=${encodeURIComponent(c |  |
| 83 | `shortStrategyDescription` | engine | 3789-3797 | 0 |  |  |  |
| 84 | `moveModelBetweenPortfolios` | mixed | 3799-3820 | 1 | y |  |  |
| 85 | `getMergedPortfolioModels` | engine | 3822-3830 | 0 |  |  |  |
| 86 | `updatePortfolioMergeUI` | view | 3832-3850 | 4 |  |  |  |
| 87 | `renderPortfolioTabs` | view | 3852-3901 | 8 |  |  | y |
| 88 | `getPersistedPortfolioViewCache` | engine | 3903-3912 | 0 |  |  | y |
| 89 | `persistPortfolioView` | engine | 3914-3922 | 0 |  |  | y |
| 90 | `rememberPortfolioView` | engine | 3924-3940 | 0 |  |  | y |
| 91 | `getLastPortfolioView` | engine | 3942-3957 | 0 |  |  | y |
| 92 | `loadPortfolioData` | engine | 3959-3998 | 0 | y |  |  |
| 93 | `fetchPortfolioData` | engine | 4000-4057 | 0 | y | ${API_BASE}/api/portfolio_day?${query} |  |
| 94 | `refreshActivePortfolioView` | mixed | 4063-4081 | 1 | y |  |  |
| 95 | `syncPortfolioViewRefresh` | engine | 4083-4090 | 0 |  |  |  |
| 96 | `repopulateActivePortfolioFromCriteria` | engine | 4096-4109 | 0 | y |  |  |
| 97 | `activatePortfolio` | mixed | 4111-4250 | 1 | y |  | y |
| 98 | `renderPortfolioList` | view | 4295-4441 | 82 |  |  |  |
| 99 | `openPortfolioModal` | view | 4443-4451 | 4 |  |  |  |
| 100 | `uniquePortfolioName` | engine | 4453-4459 | 0 |  |  |  |
| 101 | `createSimilarPortfolio` | mixed | 4461-4485 | 3 | y |  |  |
| 102 | `renderSimilarStrategyOptions` | view | 4487-4515 | 16 |  |  |  |
| 103 | `openSimilarStrategyModal` | view | 4517-4534 | 7 | y | ${API_BASE}/api/similar_strategies?date=${encodeURIComponent |  |
| 104 | `init` | view | 4536-4622 | 4 |  |  |  |
| 105 | `LIVE_DATE` | engine | 4631-4644 | 0 |  |  |  |
| 106 | `setLiveBadge` | mixed | 4646-4656 | 3 |  |  |  |
| 107 | `refreshLiveData` | mixed | 4658-4772 | 2 | y |  |  |
| 108 | `getSelectedTimeNoteEntries` | engine | 4774-4779 | 0 |  |  |  |
| 109 | `openSelectionNotesModal` | view | 4781-4804 | 22 |  |  |  |
| 110 | `tradeDateRange` | engine | 4807-4813 | 0 |  |  |  |
| 111 | `openTradesModal` | view | 4815-4965 | 33 | y | ${API_BASE}/api/model_trades?model=${encodeURIComponent(mode |  |
| 112 | `setupTradesModal` | mixed | 4967-4984 | 23 |  |  |  |
| 113 | `setSectionCollapsed` | mixed | 4987-4994 | 7 |  |  |  |
| 114 | `collapseStorageKey` | engine | 4996-4999 | 0 |  |  |  |
| 115 | `updateCollapseAllControl` | mixed | 5001-5011 | 12 |  |  |  |
| 116 | `setAllSectionsCollapsed` | mixed | 5013-5020 | 3 |  |  | y |
| 117 | `setupCollapsibleSections` | mixed | 5022-5044 | 9 |  |  | y |
| 118 | `startLiveRefresh` | engine | 5046-5053 | 0 |  |  |  |
| 119 | `syncLiveRefreshInterval` | engine | 5055-5062 | 0 |  |  |  |
| 120 | `setupDateTabs` | mixed | 5064-5079 | 4 |  |  |  |
| 121 | `setRankingCriteria` | mixed | 5084-5229 | 5 | y |  |  |
| 122 | `updateScenarioUI` | view | 5231-5243 | 3 |  |  |  |
| 123 | `renderModalScenarioCards` | view | 5245-5288 | 5 |  |  |  |
| 124 | `updateDateLabelAndTitle` | view | 5290-5312 | 9 |  |  |  |
| 125 | `setSplitMode` | engine | 5314-5322 | 0 |  |  |  |
| 126 | `syncSplitModeControls` | mixed | 5324-5341 | 6 |  |  |  |
| 127 | `getMetricKeys` | engine | 5344-5356 | 0 |  |  |  |
| 128 | `getStrategyFamily` | engine | 5358-5365 | 0 |  |  |  |
| 129 | `updateStrategyFamilyOptions` | mixed | 5367-5370 | 1 |  |  |  |
| 130 | `getScenarioCandidates` | engine | 5372-5408 | 0 |  |  |  |
| 131 | `modelSearchTerms` | engine | 5410-5412 | 0 |  |  |  |
| 132 | `getEligibleModels` | mixed | 5414-5475 | 8 |  |  |  |
| 133 | `getExactSearchModel` | engine | 5477-5485 | 0 |  |  |  |
| 134 | `loadModelSearchFromDatabase` | mixed | 5487-5543 | 6 | y | ${API_BASE}/api/portfolio_day?${params.toString()} |  |
| 135 | `loadDeepLinkModelsFromDatabase` | mixed | 5545-5590 | 4 | y | ${API_BASE}/api/portfolio_day?${params} |  |
| 136 | `getReplayTimelineModels` | engine | 5592-5612 | 0 |  |  |  |
| 137 | `pointInTimeAtReplayHead` | engine | 5614-5623 | 0 |  |  |  |
| 138 | `clockMinutes` | engine | 5625-5630 | 0 |  |  |  |
| 139 | `replayClockTime` | engine | 5632-5635 | 0 |  |  |  |
| 140 | `nextAutomaticTop1Minute` | engine | 5637-5643 | 0 |  |  |  |
| 141 | `selectedTimeRankCount` | engine | 5645-5647 | 0 |  |  |  |
| 142 | `retainSelectedTimeLeaders` | engine | 5649-5674 | 0 |  |  |  |
| 143 | `applySelectedTime` | mixed | 5676-5728 | 5 |  |  |  |
| 144 | `pointInTimeRequestOptions` | engine | 5730-5747 | 0 |  |  |  |
| 145 | `pointInTimeContextKey` | engine | 5749-5753 | 0 |  |  |  |
| 146 | `scheduleAutomaticTop1Refresh` | mixed | 5755-5801 | 2 |  |  |  |
| 147 | `renderPointInTimeHistory` | view | 5803-5836 | 8 |  |  |  |
| 148 | `refreshPointInTimeHistory` | mixed | 5838-5863 | 4 | y | ${API_BASE}/api/point_in_time_scenario_hours?${query} |  |
| 149 | `refreshPointInTimeSelection` | mixed | 5865-6068 | 11 | y | ${API_BASE}/api/point_in_time_scenario?${query} |  |
| 150 | `schedulePointInTimeSelection` | mixed | 6069-6094 | 1 |  |  |  |
| 151 | `updatePointInTimeToggleUI` | view | 6096-6125 | 7 |  |  |  |
| 152 | `getMaxFrames` | engine | 6127-6131 | 0 |  |  |  |
| 153 | `switchDate` | mixed | 6133-6216 | 2 | y |  |  |
| 154 | `updateDeltaButtonsUI` | view | 6218-6264 | 24 |  |  |  |
| 155 | `setReplaySpeed` | engine | 6269-6284 | 0 |  |  |  |
| 156 | `togglePlay` | engine | 6286-6292 | 0 |  |  |  |
| 157 | `startReplay` | mixed | 6294-6306 | 4 |  |  |  |
| 158 | `pauseReplay` | mixed | 6308-6318 | 4 |  |  |  |
| 159 | `startPlaybackLoop` | engine | 6320-6335 | 0 |  |  |  |
| 160 | `step` | engine | 6337-6346 | 0 |  |  |  |
| 161 | `seekToPct` | engine | 6348-6357 | 0 |  |  |  |
| 162 | `updateScrubberUI` | view | 6359-6400 | 18 |  |  |  |
| 163 | `storedHourlyColumns` | engine | 6420-6423 | 0 |  |  | y |
| 164 | `persistHourlyColumns` | engine | 6428-6430 | 0 |  |  | y |
| 165 | `renderHourlyColumnPanel` | view | 6432-6460 | 6 |  |  |  |
| 166 | `hourlyMetricCell` | engine | 6462-6470 | 0 |  |  |  |
| 167 | `renderHourlyRows` | view | 6472-6503 | 3 |  |  |  |
| 168 | `hourlyMoney` | engine | 6505-6508 | 0 |  |  |  |
| 169 | `hourlyTone` | engine | 6510-6512 | 0 |  |  |  |
| 170 | `hourlyIntervalLabel` | engine | 6514-6518 | 0 |  |  |  |
| 171 | `renderHourlyFamilyTabs` | view | 6520-6531 | 3 |  |  |  |
| 172 | `syncHourlyProducts` | mixed | 6533-6538 | 3 |  |  |  |
| 173 | `loadHourlyReport` | mixed | 6540-6575 | 15 | y | ${API_BASE}/api/hourly_family_report?${query} |  |
| 174 | `openHourlyReport` | view | 6577-6593 | 3 |  |  |  |
| 175 | `closeHourlyReport` | view | 6595-6599 | 1 |  |  |  |
| 176 | `updateChartLockControlState` | engine | 6601-6610 | 0 |  |  |  |
| 177 | `applyChartLock` | mixed | 6612-6640 | 5 |  |  |  |
| 178 | `setupEventListeners` | mixed | 6642-7269 | 150 |  |  | y |
| 179 | `getBasePoint` | engine | 7271-7284 | 0 |  |  |  |
| 180 | `getReplayHeadPoint` | engine | 7286-7292 | 0 |  |  |  |
| 181 | `updateRibbon` | mixed | 7294-7379 | 24 |  |  |  |
| 182 | `renderCards` | view | 7381-7529 | 7 |  |  |  |
| 183 | `setupCanvas` | mixed | 7531-7543 | 2 |  |  |  |
| 184 | `computeTradeOverlaySignals` | engine | 7562-7704 | 0 |  |  |  |
| 185 | `pairOverlayTrades` | engine | 7708-7742 | 0 |  |  |  |
| 186 | `computeSplitTargetSignal` | engine | 7746-7783 | 0 |  |  |  |
| 187 | `modelPointAtOrBeforeTime` | engine | 7785-7795 | 0 |  |  |  |
| 188 | `selectedTimeJoinAt` | engine | 7797-7800 | 0 |  |  |  |
| 189 | `selectedTimeModelEligibleAt` | engine | 7802-7805 | 0 |  |  |  |
| 190 | `selectedTimePointEligible` | engine | 7807-7809 | 0 |  |  |  |
| 191 | `computeLeaderRotation` | engine | 7815-7973 | 0 |  |  |  |
| 192 | `computeMultiSplitRotation` | engine | 7978-8153 | 0 |  |  |  |
| 193 | `drawLeaderSignalBadge` | engine | 8155-8170 | 0 |  |  |  |
| 194 | `showTargetPulse` | view | 8172-8182 | 7 |  |  |  |
| 195 | `drawTradeValueLabel` | engine | 8184-8203 | 0 |  |  |  |
| 196 | `updateOverlayTradeSummary` | mixed | 8205-8231 | 9 |  |  |  |
| 197 | `openOverlayTradesModal` | view | 8233-8350 | 21 | y |  |  |
| 198 | `drawSignalBadge` | engine | 8352-8380 | 0 |  |  |  |
| 199 | `drawChart` | view | 8382-8645 | 3 |  |  |  |
| 200 | `scheduleDashboardUtilityRuntime` | mixed | 8648-8656 | 1 |  |  |  |
| 201 | `drawBaselineMarker` | engine | 8658-8672 | 0 |  |  |  |
| 202 | `drawReplayCursor` | engine | 8674-8688 | 0 |  |  |  |
| 203 | `renderDeltaLine` | engine | 8690-8704 | 0 |  |  |  |
| 204 | `drawPointLabel` | engine | 8706-8715 | 0 |  |  |  |
| 205 | `drawGridAndAxes` | engine | 8717-8762 | 0 |  |  |  |

## State variables

- `API_BASE` (const, line 1426)
- `SCENARIOS_CATALOGUE` (const, line 1428)
- `MOMENTUM_SCENARIO_IDS` (const, line 1437)
- `ALL_CRITERIA_DATA` (const, line 1438)
- `FAMILY_TOP_FIVE_SCENARIOS` (const, line 1474)
- `TP_SL_SCENARIO_IDS` (const, line 1496)
- `ALL_DATE_DATA` (const, line 1530)
- `LIVE_CHART_CACHE_PREFIX` (const, line 1531)
- `LIVE_CHART_CACHE_TTL_MS` (const, line 1532)
- `LIVE_CHART_CACHE_MAX_BYTES` (const, line 1533)
- `initialLiveDataAvailable` (let, line 1534)
- `liveChartDataLoadedKeys` (const, line 1535)
- `cachedProductsForLive` (let, line 1583)
- `historicalCurveLoads` (const, line 1616)
- `currentReturnType` (let, line 1639)
- `currentCriteria` (let, line 1640)
- `mainScenarioCriteria` (let, line 1641)
- `portfolioCriteria` (let, line 1642)
- `portfolioViewConfigs` (let, line 1643)
- `mainScenarioViewConfig` (let, line 1644)
- `portfolioScenarioConfigs` (let, line 1647)
- `currentProductType` (let, line 1649)
- `currentProduct` (let, line 1651)
- `currentStrategyFamily` (let, line 1652)
- `modelLimit` (let, line 1653)
- `portfolios` (let, line 1654)
- `livePortfolioStore` (let, line 1655)
- `livePortfolioActiveModels` (const, line 1656)
- `overlayRuleLibrary` (let, line 1657)
- `assignedOverlayTradeCache` (const, line 1658)
- `assignedOverlayTradeRequests` (const, line 1659)
- `useAssignedOverlayRule` (let, line 1660)
- `overlayRuleLibraryRequest` (let, line 1661)
- `pendingNamedOverlayRuleConfig` (let, line 1662)
- `editingNamedOverlayRuleId` (let, line 1663)
- `activePortfolioName` (let, line 1664)
- `liveModePriorChartLock` (let, line 1665)
- `liveModeRequestInFlight` (let, line 1666)
- `liveModeStatusMessages` (let, line 1667)
- `portfolioModels` (let, line 1668)
- `pendingFilterDataRefresh` (let, line 1669)
- `lastChartFallbackModels` (let, line 1670)
- `lastChartFallbackContext` (let, line 1671)
- `PORTFOLIO_VIEW_CACHE` (const, line 1674)
- `PORTFOLIO_VIEW_CACHE_MAX` (const, line 1675)
- `PORTFOLIO_VIEW_CACHE_STORAGE_KEY` (const, line 1676)
- `PORTFOLIO_VIEW_PERSIST_MAX` (const, line 1677)
- `PORTFOLIO_VIEW_REQUESTS` (const, line 1678)
- `persistedPortfolioViewCache` (let, line 1679)
- `PORTFOLIO_LAST_VIEW_CACHE` (const, line 1680)
- `portfolioTargetModel` (let, line 1681)
- `portfolioMergeSelection` (const, line 1682)
- `similarStrategyPayload` (let, line 1683)
- `strategyCatalogue` (let, line 1684)
- `strategyCatalogueDate` (let, line 1685)
- `displayTheme` (let, line 1686)
- `liveRefreshSequence` (let, line 1687)
- `liveRefreshTimer` (let, line 1688)
- `liveRefreshIntervalMs` (let, line 1689)
- `portfolioViewRefreshTimer` (let, line 1690)
- `portfolioViewRefreshInFlight` (let, line 1691)
- `PORTFOLIO_VIEW_REFRESH_MS` (const, line 1694)
- `currentDate` (let, line 1697)
- `splitMode` (let, line 1698)
- `modelSearchLoadedModels` (let, line 1700)
- `pinnedComparisonModels` (const, line 1701)
- `modelSearchRequestSequence` (let, line 1702)
- `modelSearchTimer` (let, line 1703)
- `deepLinkModel` (let, line 1704)
- `deepLinkModels` (let, line 1705)
- `deepLinkModelsOnly` (let, line 1706)
- `deepLinkDate` (let, line 1707)
- `selectedModelIndex` (let, line 1708)
- `baselineFrameIndex` (let, line 1709)
- `currentFrameIndex` (let, line 1710)
- `minWinRate` (let, line 1711)
- `visibleModels` (let, line 1712)
- `scenarioRemovedModels` (const, line 1715)
- `POINT_IN_TIME_SELECTION_STORAGE_KEY` (const, line 1716)
- `SELECTED_TIME_RANK_STORAGE_KEY` (const, line 1717)
- `pointInTimeSelectionPreference` (let, line 1718)
- `pointInTimeMode` (let, line 1719)
- `top1AtTimePreviousPointInTimeMode` (let, line 1720)
- `pointInTimeModels` (let, line 1721)
- `pointInTimeRequestSequence` (let, line 1722)
- `pointInTimeRequestedKey` (let, line 1723)
- `pointInTimeDebounceTimer` (let, line 1724)
- `pointInTimeHours` (let, line 1725)
- `pointInTimeHistoryKey` (let, line 1726)
- `pointInTimeHistorySequence` (let, line 1727)
- `pointInTimeHistoryAt` (let, line 1728)
- `pendingExplicitTop1Time` (let, line 1729)
- `selectedTimeLeaderHistory` (const, line 1730)
- `selectedTimeLeaderHistoryContext` (let, line 1731)
- `selectedTimeExplicitRefresh` (let, line 1732)
- `autoRefreshTop1Enabled` (let, line 1733)
- `autoRefreshTop1Minutes` (let, line 1734)
- `autoRefreshTop1Direction` (let, line 1735)
- `autoRefreshTop1Rank` (let, line 1736)
- `autoRefreshTop1LastMinute` (let, line 1737)
- `autoRefreshTop1NextMinute` (let, line 1738)
- `autoRefreshTop1Context` (let, line 1739)
- `autoRefreshTop1RequestAt` (let, line 1740)
- `showNetDelta` (let, line 1743)
- `showBuyDelta` (let, line 1744)
- `showSellDelta` (let, line 1745)
- `showTradeMarkers` (let, line 1746)
- `showTradeValues` (let, line 1747)
- `lastOverlayTrades` (let, line 1748)
- `exitThreshold` (let, line 1749)
- `overlayTopX` (let, line 1750)
- `dailyTarget` (let, line 1751)
- `hourlyReportFamily` (let, line 1752)
- `hourlyReportDate` (let, line 1753)
- `hourlyReportTimer` (let, line 1754)
- `hourlyReportRequest` (let, line 1755)
- `hourlyReportPayload` (let, line 1756)
- `hourlyReportInterval` (let, line 1757)
- `chartLocked` (let, line 1761)
- `isPlaying` (let, line 1766)
- `replayInterval` (let, line 1767)
- `replaySpeed` (let, line 1768)
- `BASE_INTERVAL_MS` (const, line 1769)
- `returnTypeNetBtn` (const, line 1785)
- `returnTypeAltBtn` (const, line 1786)
- `openScenarioModalBtn` (const, line 1787)
- `closeScenarioModalBtn` (const, line 1788)
- `closeScenarioModalFooterBtn` (const, line 1789)
- `scenarioModal` (const, line 1790)
- `modalScenarioCards` (const, line 1791)
- `scenarioSearchInput` (const, line 1792)
- `activeScenarioIcon` (const, line 1793)
- `activeScenarioName` (const, line 1794)
- `activeCriteriaLabel` (const, line 1795)
- `dateTabsContainer` (const, line 1797)
- `productTypeFilter` (const, line 1798)
- `productFilter` (const, line 1799)
- `strategyFamilyFilter` (const, line 1800)
- `modelLimitFilter` (const, line 1801)
- `modelSearchInput` (const, line 1802)
- `modelSearchStatus` (const, line 1803)
- `portfolioTabs` (const, line 1804)
- `portfolioModal` (const, line 1805)
- `savePortfolioWorkspaceBtn` (const, line 1806)
- `portfolioWorkspaceSaveStatus` (const, line 1807)
- `overlayRuleLibraryModal` (const, line 1808)
- `overlayRuleNameModal` (const, line 1809)
- `liveRuleStatus` (const, line 1810)
- `livePortfolioTransitionBanner` (const, line 1811)
- `portfolioList` (const, line 1812)
- `mergePortfolioForm` (const, line 1813)
- `mergePortfolioBtn` (const, line 1814)
- `mergePortfolioSummary` (const, line 1815)
- `mergePortfolioCount` (const, line 1816)
- `selectAllPortfoliosBtn` (const, line 1817)
- `deleteSelectedPortfoliosBtn` (const, line 1818)
- `strategyCataloguePanel` (const, line 1819)
- `strategyCatalogueResults` (const, line 1820)
- `catalogPortfolioFilter` (const, line 1821)
- `catalogTypeFilter` (const, line 1822)
- `catalogProductFilter` (const, line 1823)
- `catalogFamilyFilter` (const, line 1824)
- `catalogWindowFilter` (const, line 1825)
- `catalogTpFilter` (const, line 1826)
- `catalogSlFilter` (const, line 1827)
- `similarStrategyModal` (const, line 1828)
- `similarStrategyContext` (const, line 1829)
- `similarStrategyOptions` (const, line 1830)
- `themeToggle` (const, line 1831)
- `openHourlyReportBtn` (const, line 1832)
- `hourlyReportModal` (const, line 1833)
- `hourlyProductType` (const, line 1834)
- `hourlyProduct` (const, line 1835)
- `hourlyInterval` (const, line 1836)
- `hourlyFamilyTabs` (const, line 1837)
- `hourlyReportHead` (const, line 1838)
- `hourlyReportBody` (const, line 1839)
- `hourlyReportSummary` (const, line 1840)
- `hourlyColumnToggle` (const, line 1841)
- `hourlyColumnPanel` (const, line 1842)
- `activeDateLabel` (const, line 1843)
- `winRateDisplayBadge` (const, line 1844)
- `replayStartBadge` (const, line 1845)
- `cardsGridTitle` (const, line 1846)
- `canvas` (const, line 1847)
- `ctx` (const, line 1848)
- `tooltip` (const, line 1849)
- `modelCardsContainer` (const, line 1850)
- `metricAll` (const, line 1852)
- `metricBuy` (const, line 1853)
- `metricSell` (const, line 1854)
- `metricTriSplit` (const, line 1855)
- `metricMultiSplit` (const, line 1856)
- `showAllBtn` (const, line 1858)
- `hideAllBtn` (const, line 1859)
- `clearHiddenBtn` (const, line 1860)
- `clearAllStrategiesBtn` (const, line 1861)
- `playBtn` (const, line 1864)
- `playIcon` (const, line 1865)
- `playBtnText` (const, line 1866)
- `stepBackBtn` (const, line 1867)
- `stepFwdBtn` (const, line 1868)
- `restartBtn` (const, line 1869)
- `speed1x` (const, line 1870)
- `speed025x` (const, line 1871)
- `speed05x` (const, line 1872)
- `speed3x` (const, line 1873)
- `speed10x` (const, line 1874)
- `replayTimeBadge` (const, line 1876)
- `replayProgressPercent` (const, line 1877)
- `baselineTimeBadge` (const, line 1878)
- `selectedTimeForm` (const, line 1879)
- `selectedTimeRankSelect` (const, line 1880)
- `selectedTimeInput` (const, line 1881)
- `applySelectedTimeBtn` (const, line 1882)
- `autoRefreshTop1Toggle` (const, line 1883)
- `autoRefreshTop1Interval` (const, line 1884)
- `autoRefreshTop1DirectionSelect` (const, line 1885)
- `autoRefreshTop1RankSelect` (const, line 1886)
- `autoRefreshTop1Status` (const, line 1887)
- `savedSelectedTimeRank` (const, line 1888)
- `setBaseAtHeadBtn` (const, line 1909)
- `resetBaselineBtn` (const, line 1910)
- `chartLockBtn` (const, line 1911)
- `chartLockIcon` (const, line 1912)
- `chartLockLabel` (const, line 1913)
- `liveModeBtn` (const, line 1914)
- `liveModeLabel` (const, line 1915)
- `scrubberTrack` (const, line 1917)
- `scrubberFill` (const, line 1918)
- `scrubberThumb` (const, line 1919)
- `baselineMarker` (const, line 1920)
- `baselineBadge` (const, line 1921)
- `winRateSlider` (const, line 1923)
- `winRateValBadge` (const, line 1924)
- `toggleNetDeltaBtn` (const, line 1927)
- `pointInTimeToggle` (const, line 1928)
- `pointInTimeStatus` (const, line 1929)
- `pointInTimeHistoryPanel` (const, line 2041)
- `pointInTimeHistoryStatus` (const, line 2042)
- `pointInTimeHistoryRows` (const, line 2043)
- `pointInTimeHistoryNearViewport` (let, line 2044)
- `toggleBuyDeltaBtn` (const, line 2054)
- `toggleSellDeltaBtn` (const, line 2055)
- `netDeltaCheck` (const, line 2056)
- `buyDeltaCheck` (const, line 2057)
- `sellDeltaCheck` (const, line 2058)
- `toggleTradeMarkersBtn` (const, line 2059)
- `tradeMarkersCheck` (const, line 2060)
- `ribbonModelName` (const, line 2062)
- `ribbonProduct` (const, line 2063)
- `ribbonStrategy` (const, line 2064)
- `ribbonTotNet` (const, line 2065)
- `ribbonBuyNet` (const, line 2066)
- `ribbonSellNet` (const, line 2067)
- `totalNetLabel` (const, line 2068)
- `buyNetLabel` (const, line 2069)
- `sellNetLabel` (const, line 2070)
- `indicatorBar` (const, line 2071)
- `portfolioWorkspaceStorageKeys` (const, line 2221)
- `liveActivationModal` (const, line 3115)
- `liveActivationForm` (const, line 3116)
- `liveActivationRule` (const, line 3117)
- `LIVE_REFRESH_MS` (const, line 4627)
- `LIVE_MODE_REFRESH_MS` (const, line 4628)
- `HOURLY_REPORT_FAMILIES` (const, line 6402)
- `HOURLY_COLUMN_PREF_KEY` (const, line 6407)
- `HOURLY_METRICS` (const, line 6408)
- `HOURLY_COLUMNS` (const, line 6414)
- `hourlyVisibleColumns` (let, line 6424)
- `timeAxisPoints` (let, line 7545)
- `dashboardUtilityRuntimeScheduled` (let, line 8647)
