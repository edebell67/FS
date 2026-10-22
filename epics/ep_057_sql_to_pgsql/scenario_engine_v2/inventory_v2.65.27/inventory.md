# Inventory of top10_5min_equity_curves (snapshot v2.65.24)

Source: `top10_5min_equity_curves_source_v2.65.27.html`; main script lines 1427-9000.

- functions: **205** (engine 110, view 38, mixed 57)
- top-level state variables: **273**
- top-level wiring statements: **5**

Classification is a heuristic: `engine` = no DOM references; `view` = DOM references and a render/UI-style name; `mixed` = DOM references and an unclear name, needing a manual split in the engine-core task.

| # | function | kind | lines | DOM refs | async | fetch | storage |
|---|---|---|---|---|---|---|---|
| 1 | `syncTpSlScenarios` | engine | 1500-1521 | 0 |  |  |  |
| 2 | `isMetricAwareCriteria` | engine | 1522-1531 | 0 |  |  |  |
| 3 | `liveChartCacheKey` | engine | 1539-1544 | 0 |  |  |  |
| 4 | `restoreLiveChartCache` | engine | 1545-1564 | 0 |  |  | y |
| 5 | `paintLiveChartCache` | engine | 1565-1573 | 0 |  |  |  |
| 6 | `scheduleLiveChartCacheFallback` | engine | 1574-1585 | 0 |  |  |  |
| 7 | `cacheLiveChartResponse` | engine | 1587-1618 | 0 |  |  | y |
| 8 | `ensureHistoricalDataLoaded` | engine | 1620-1638 | 0 | y |  |  |
| 9 | `availableDates` | engine | 1778-1789 | 0 |  |  |  |
| 10 | `triggerSelectedTimeRefresh` | mixed | 1903-1911 | 1 |  |  |  |
| 11 | `updateAutoRefreshTop1Status` | view | 1943-1948 | 1 |  |  |  |
| 12 | `finishAutomaticTop1Refresh` | engine | 1949-1966 | 0 |  |  |  |
| 13 | `resetAutomaticRankSchedule` | mixed | 1979-2000 | 1 |  |  |  |
| 14 | `setReturnType` | engine | 2084-2124 | 0 |  |  |  |
| 15 | `setReturnType` | engine | 2130-2193 | 0 |  |  | y |
| 16 | `syncLiveAltReporting` | engine | 2195-2201 | 0 |  |  |  |
| 17 | `savePortfolios` | engine | 2203-2206 | 0 |  |  | y |
| 18 | `movePortfolio` | engine | 2208-2220 | 0 |  |  |  |
| 19 | `saveCriteriaWorkspaces` | engine | 2222-2226 | 0 |  |  | y |
| 20 | `savePortfolioWorkspaceToPostgres` | mixed | 2235-2263 | 3 | y | ${API_BASE}/api/scenario_workspace | y |
| 21 | `restorePortfolioWorkspaceFromPostgres` | mixed | 2265-2290 | 1 | y | ${API_BASE}/api/scenario_workspace | y |
| 22 | `currentPortfolioViewConfig` | engine | 2292-2310 | 0 |  |  |  |
| 23 | `persistPortfolioViewConfig` | engine | 2312-2320 | 0 |  |  | y |
| 24 | `applyPortfolioViewConfig` | mixed | 2322-2376 | 14 |  |  |  |
| 25 | `loadLivePortfolioStore` | engine | 2378-2387 | 0 | y | ${location.origin}/api/live_portfolios |  |
| 26 | `livePortfolioModelsForDate` | engine | 2389-2419 | 0 |  |  |  |
| 27 | `autoPinLivePortfolioStrategies` | engine | 2421-2429 | 0 |  |  |  |
| 28 | `loadOverlayRuleLibrary` | engine | 2431-2448 | 0 | y | ${API_BASE}/api/overlay_rules |  |
| 29 | `assignedPortfolioOverlayRule` | engine | 2450-2454 | 0 |  |  |  |
| 30 | `activePortfolioOverlayRule` | engine | 2456-2459 | 0 |  |  |  |
| 31 | `syncAssignedOverlayRuleUI` | view | 2461-2480 | 9 |  |  |  |
| 32 | `overlayRuleSummary` | engine | 2482-2495 | 0 |  |  |  |
| 33 | `overlayRuleMetricValue` | engine | 2497-2516 | 0 |  |  |  |
| 34 | `renderOverlayRuleLibrary` | view | 2518-2569 | 40 |  |  |  |
| 35 | `beginEditNamedOverlayRule` | mixed | 2571-2598 | 33 |  |  |  |
| 36 | `cancelEditNamedOverlayRule` | mixed | 2600-2606 | 9 |  |  |  |
| 37 | `overlayRuleCandidate` | engine | 2608-2713 | 0 |  |  |  |
| 38 | `asOfCorrelation` | engine | 2715-2730 | 0 |  |  |  |
| 39 | `assignedOverlayTradeCacheKey` | engine | 2732-2734 | 0 |  |  |  |
| 40 | `ensureAssignedOverlayTradeData` | engine | 2736-2767 | 0 | y |  |  |
| 41 | `timeOfDayMinutes` | engine | 2769-2772 | 0 |  |  |  |
| 42 | `curvePointAtOrBefore` | engine | 2774-2784 | 0 |  |  |  |
| 43 | `sourceTradeFlipResults` | engine | 2786-2810 | 0 |  |  |  |
| 44 | `applyAssignedOverlayTradeResults` | engine | 2812-2878 | 0 |  |  |  |
| 45 | `assignedRuleTarget` | engine | 2880-2898 | 0 |  |  |  |
| 46 | `openOverlayRuleLibrary` | view | 2900-2904 | 1 | y |  |  |
| 47 | `configFromOverlayEditor` | mixed | 2906-2921 | 16 |  |  |  |
| 48 | `openNamedOverlayRuleSave` | view | 2923-2937 | 17 |  |  |  |
| 49 | `saveNamedOverlayRule` | mixed | 2939-2978 | 21 | y |  |  |
| 50 | `assignOverlayRule` | mixed | 2980-3003 | 8 | y | ${API_BASE}/api/overlay_rules/assignments/${encodeURICompone |  |
| 51 | `renderLivePortfolioTransition` | view | 3005-3031 | 3 |  |  |  |
| 52 | `isLiveModePortfolio` | engine | 3033-3035 | 0 |  |  |  |
| 53 | `isLiveModeArmed` | engine | 3037-3040 | 0 |  |  |  |
| 54 | `syncStrategyRemovalButtons` | view | 3042-3061 | 4 |  |  |  |
| 55 | `syncLiveModeUI` | view | 3063-3120 | 12 |  |  |  |
| 56 | `liveActivationRulesReady` | engine | 3126-3133 | 0 |  |  |  |
| 57 | `liveActivationRuleLabel` | engine | 3135-3149 | 0 |  |  |  |
| 58 | `syncLiveActivationReview` | view | 3151-3191 | 44 |  |  |  |
| 59 | `showLiveActivationReview` | view | 3193-3217 | 27 | y |  |  |
| 60 | `activateLiveModeFromReview` | mixed | 3219-3311 | 38 | y | ${location.origin}/api/live_portfolios/config |  |
| 61 | `toggleLiveMode` | view | 3313-3362 | 3 | y | ${location.origin}/api/live_portfolios/config |  |
| 62 | `loadLivePortfolioRulesIntoForm` | mixed | 3364-3392 | 19 | y |  |  |
| 63 | `isRuleManagedLivePortfolio` | engine | 3394-3396 | 0 |  |  |  |
| 64 | `liveRuleSummary` | engine | 3398-3418 | 0 |  |  |  |
| 65 | `appendRuleDetailsSection` | mixed | 3420-3449 | 18 |  |  |  |
| 66 | `showLivePortfolioRuleDetails` | view | 3451-3502 | 12 | y |  |  |
| 67 | `editLivePortfolioRules` | mixed | 3504-3511 | 9 | y |  |  |
| 68 | `syncLivePortfolioScreenState` | mixed | 3513-3547 | 1 | y |  |  |
| 69 | `saveLivePortfolioRules` | mixed | 3549-3593 | 24 | y | ${location.origin}/api/live_portfolios/config |  |
| 70 | `portfolioScenarioConfig` | engine | 3595-3597 | 0 |  |  |  |
| 71 | `capturePortfolioScenario` | engine | 3599-3609 | 0 |  |  | y |
| 72 | `markPortfolioFixed` | engine | 3611-3622 | 0 |  |  |  |
| 73 | `applyDisplayTheme` | mixed | 3624-3634 | 9 |  |  | y |
| 74 | `removeModelFromPortfolio` | engine | 3636-3650 | 0 | y |  |  |
| 75 | `deletePortfolio` | mixed | 3652-3655 | 1 | y |  |  |
| 76 | `deleteSelectedPortfolios` | mixed | 3657-3665 | 1 | y |  |  |
| 77 | `removePortfolios` | engine | 3667-3692 | 0 | y |  | y |
| 78 | `setCatalogueOptions` | mixed | 3694-3702 | 9 |  |  |  |
| 79 | `populateCataloguePortfolioOptions` | mixed | 3704-3712 | 6 |  |  |  |
| 80 | `addCatalogueModel` | mixed | 3714-3734 | 1 | y |  |  |
| 81 | `renderStrategyCatalogue` | view | 3736-3774 | 17 |  |  |  |
| 82 | `loadStrategyCatalogue` | mixed | 3776-3794 | 2 | y | ${API_BASE}/api/strategy_catalog?date=${encodeURIComponent(c |  |
| 83 | `shortStrategyDescription` | engine | 3796-3804 | 0 |  |  |  |
| 84 | `moveModelBetweenPortfolios` | mixed | 3806-3827 | 1 | y |  |  |
| 85 | `getMergedPortfolioModels` | engine | 3829-3837 | 0 |  |  |  |
| 86 | `updatePortfolioMergeUI` | view | 3839-3857 | 4 |  |  |  |
| 87 | `renderPortfolioTabs` | view | 3859-3908 | 8 |  |  | y |
| 88 | `getPersistedPortfolioViewCache` | engine | 3910-3919 | 0 |  |  | y |
| 89 | `persistPortfolioView` | engine | 3921-3929 | 0 |  |  | y |
| 90 | `rememberPortfolioView` | engine | 3931-3947 | 0 |  |  | y |
| 91 | `getLastPortfolioView` | engine | 3949-3964 | 0 |  |  | y |
| 92 | `loadPortfolioData` | engine | 3966-4005 | 0 | y |  |  |
| 93 | `fetchPortfolioData` | engine | 4007-4064 | 0 | y | ${API_BASE}/api/portfolio_day?${query} |  |
| 94 | `refreshActivePortfolioView` | mixed | 4070-4088 | 1 | y |  |  |
| 95 | `syncPortfolioViewRefresh` | engine | 4090-4097 | 0 |  |  |  |
| 96 | `repopulateActivePortfolioFromCriteria` | engine | 4103-4116 | 0 | y |  |  |
| 97 | `activatePortfolio` | mixed | 4118-4257 | 1 | y |  | y |
| 98 | `renderPortfolioList` | view | 4302-4448 | 82 |  |  |  |
| 99 | `openPortfolioModal` | view | 4450-4458 | 4 |  |  |  |
| 100 | `uniquePortfolioName` | engine | 4460-4466 | 0 |  |  |  |
| 101 | `createSimilarPortfolio` | mixed | 4468-4492 | 3 | y |  |  |
| 102 | `renderSimilarStrategyOptions` | view | 4494-4522 | 16 |  |  |  |
| 103 | `openSimilarStrategyModal` | view | 4524-4541 | 7 | y | ${API_BASE}/api/similar_strategies?date=${encodeURIComponent |  |
| 104 | `init` | view | 4543-4629 | 4 |  |  |  |
| 105 | `LIVE_DATE` | engine | 4638-4651 | 0 |  |  |  |
| 106 | `setLiveBadge` | mixed | 4653-4663 | 3 |  |  |  |
| 107 | `refreshLiveData` | mixed | 4665-4779 | 2 | y |  |  |
| 108 | `getSelectedTimeNoteEntries` | engine | 4781-4786 | 0 |  |  |  |
| 109 | `openSelectionNotesModal` | view | 4788-4811 | 22 |  |  |  |
| 110 | `tradeDateRange` | engine | 4814-4820 | 0 |  |  |  |
| 111 | `openTradesModal` | view | 4822-4972 | 33 | y | ${API_BASE}/api/model_trades?model=${encodeURIComponent(mode |  |
| 112 | `setupTradesModal` | mixed | 4974-4991 | 23 |  |  |  |
| 113 | `setSectionCollapsed` | mixed | 4994-5001 | 7 |  |  |  |
| 114 | `collapseStorageKey` | engine | 5003-5006 | 0 |  |  |  |
| 115 | `updateCollapseAllControl` | mixed | 5008-5018 | 12 |  |  |  |
| 116 | `setAllSectionsCollapsed` | mixed | 5020-5027 | 3 |  |  | y |
| 117 | `setupCollapsibleSections` | mixed | 5029-5051 | 9 |  |  | y |
| 118 | `startLiveRefresh` | engine | 5053-5060 | 0 |  |  |  |
| 119 | `syncLiveRefreshInterval` | engine | 5062-5069 | 0 |  |  |  |
| 120 | `setupDateTabs` | mixed | 5071-5086 | 4 |  |  |  |
| 121 | `setRankingCriteria` | mixed | 5091-5236 | 5 | y |  |  |
| 122 | `updateScenarioUI` | view | 5238-5250 | 3 |  |  |  |
| 123 | `renderModalScenarioCards` | view | 5252-5295 | 5 |  |  |  |
| 124 | `updateDateLabelAndTitle` | view | 5297-5319 | 9 |  |  |  |
| 125 | `setSplitMode` | engine | 5321-5329 | 0 |  |  |  |
| 126 | `syncSplitModeControls` | mixed | 5331-5348 | 6 |  |  |  |
| 127 | `getMetricKeys` | engine | 5351-5363 | 0 |  |  |  |
| 128 | `getStrategyFamily` | engine | 5365-5372 | 0 |  |  |  |
| 129 | `updateStrategyFamilyOptions` | mixed | 5374-5377 | 1 |  |  |  |
| 130 | `getScenarioCandidates` | engine | 5379-5415 | 0 |  |  |  |
| 131 | `modelSearchTerms` | engine | 5417-5419 | 0 |  |  |  |
| 132 | `getEligibleModels` | mixed | 5421-5482 | 8 |  |  |  |
| 133 | `getExactSearchModel` | engine | 5484-5492 | 0 |  |  |  |
| 134 | `loadModelSearchFromDatabase` | mixed | 5494-5550 | 6 | y | ${API_BASE}/api/portfolio_day?${params.toString()} |  |
| 135 | `loadDeepLinkModelsFromDatabase` | mixed | 5552-5597 | 4 | y | ${API_BASE}/api/portfolio_day?${params} |  |
| 136 | `getReplayTimelineModels` | engine | 5599-5623 | 0 |  |  |  |
| 137 | `pointInTimeAtReplayHead` | engine | 5625-5634 | 0 |  |  |  |
| 138 | `clockMinutes` | engine | 5636-5641 | 0 |  |  |  |
| 139 | `replayClockTime` | engine | 5643-5646 | 0 |  |  |  |
| 140 | `nextAutomaticTop1Minute` | engine | 5648-5654 | 0 |  |  |  |
| 141 | `selectedTimeRankCount` | engine | 5656-5658 | 0 |  |  |  |
| 142 | `retainSelectedTimeLeaders` | engine | 5660-5685 | 0 |  |  |  |
| 143 | `applySelectedTime` | mixed | 5687-5739 | 5 |  |  |  |
| 144 | `pointInTimeRequestOptions` | engine | 5741-5758 | 0 |  |  |  |
| 145 | `pointInTimeContextKey` | engine | 5760-5764 | 0 |  |  |  |
| 146 | `scheduleAutomaticTop1Refresh` | mixed | 5766-5812 | 2 |  |  |  |
| 147 | `renderPointInTimeHistory` | view | 5814-5847 | 8 |  |  |  |
| 148 | `refreshPointInTimeHistory` | mixed | 5849-5874 | 4 | y | ${API_BASE}/api/point_in_time_scenario_hours?${query} |  |
| 149 | `refreshPointInTimeSelection` | mixed | 5876-6086 | 11 | y | ${API_BASE}/api/point_in_time_scenario?${query} |  |
| 150 | `schedulePointInTimeSelection` | mixed | 6087-6112 | 1 |  |  |  |
| 151 | `updatePointInTimeToggleUI` | view | 6114-6143 | 7 |  |  |  |
| 152 | `getMaxFrames` | engine | 6145-6149 | 0 |  |  |  |
| 153 | `switchDate` | mixed | 6151-6237 | 2 | y |  |  |
| 154 | `updateDeltaButtonsUI` | view | 6239-6285 | 24 |  |  |  |
| 155 | `setReplaySpeed` | engine | 6290-6305 | 0 |  |  |  |
| 156 | `togglePlay` | engine | 6307-6313 | 0 |  |  |  |
| 157 | `startReplay` | mixed | 6315-6327 | 4 |  |  |  |
| 158 | `pauseReplay` | mixed | 6329-6339 | 4 |  |  |  |
| 159 | `startPlaybackLoop` | engine | 6341-6356 | 0 |  |  |  |
| 160 | `step` | engine | 6358-6367 | 0 |  |  |  |
| 161 | `seekToPct` | engine | 6369-6378 | 0 |  |  |  |
| 162 | `updateScrubberUI` | view | 6380-6421 | 18 |  |  |  |
| 163 | `storedHourlyColumns` | engine | 6441-6444 | 0 |  |  | y |
| 164 | `persistHourlyColumns` | engine | 6449-6451 | 0 |  |  | y |
| 165 | `renderHourlyColumnPanel` | view | 6453-6481 | 6 |  |  |  |
| 166 | `hourlyMetricCell` | engine | 6483-6491 | 0 |  |  |  |
| 167 | `renderHourlyRows` | view | 6493-6524 | 3 |  |  |  |
| 168 | `hourlyMoney` | engine | 6526-6529 | 0 |  |  |  |
| 169 | `hourlyTone` | engine | 6531-6533 | 0 |  |  |  |
| 170 | `hourlyIntervalLabel` | engine | 6535-6539 | 0 |  |  |  |
| 171 | `renderHourlyFamilyTabs` | view | 6541-6552 | 3 |  |  |  |
| 172 | `syncHourlyProducts` | mixed | 6554-6559 | 3 |  |  |  |
| 173 | `loadHourlyReport` | mixed | 6561-6596 | 15 | y | ${API_BASE}/api/hourly_family_report?${query} |  |
| 174 | `openHourlyReport` | view | 6598-6614 | 3 |  |  |  |
| 175 | `closeHourlyReport` | view | 6616-6620 | 1 |  |  |  |
| 176 | `updateChartLockControlState` | engine | 6622-6631 | 0 |  |  |  |
| 177 | `applyChartLock` | mixed | 6633-6661 | 5 |  |  |  |
| 178 | `setupEventListeners` | mixed | 6663-7294 | 150 |  |  | y |
| 179 | `getBasePoint` | engine | 7296-7309 | 0 |  |  |  |
| 180 | `getReplayHeadPoint` | engine | 7311-7317 | 0 |  |  |  |
| 181 | `updateRibbon` | mixed | 7319-7404 | 24 |  |  |  |
| 182 | `renderCards` | view | 7406-7554 | 7 |  |  |  |
| 183 | `setupCanvas` | mixed | 7556-7568 | 2 |  |  |  |
| 184 | `computeTradeOverlaySignals` | engine | 7587-7729 | 0 |  |  |  |
| 185 | `pairOverlayTrades` | engine | 7733-7767 | 0 |  |  |  |
| 186 | `computeSplitTargetSignal` | engine | 7771-7808 | 0 |  |  |  |
| 187 | `modelPointAtOrBeforeTime` | engine | 7810-7820 | 0 |  |  |  |
| 188 | `selectedTimeJoinAt` | engine | 7822-7825 | 0 |  |  |  |
| 189 | `selectedTimeModelEligibleAt` | engine | 7827-7830 | 0 |  |  |  |
| 190 | `selectedTimePointEligible` | engine | 7832-7834 | 0 |  |  |  |
| 191 | `computeLeaderRotation` | engine | 7840-7998 | 0 |  |  |  |
| 192 | `computeMultiSplitRotation` | engine | 8003-8178 | 0 |  |  |  |
| 193 | `drawLeaderSignalBadge` | engine | 8180-8195 | 0 |  |  |  |
| 194 | `showTargetPulse` | view | 8197-8207 | 7 |  |  |  |
| 195 | `drawTradeValueLabel` | engine | 8209-8228 | 0 |  |  |  |
| 196 | `updateOverlayTradeSummary` | mixed | 8230-8256 | 9 |  |  |  |
| 197 | `openOverlayTradesModal` | view | 8258-8375 | 21 | y |  |  |
| 198 | `drawSignalBadge` | engine | 8377-8405 | 0 |  |  |  |
| 199 | `drawChart` | view | 8407-8670 | 3 |  |  |  |
| 200 | `scheduleDashboardUtilityRuntime` | mixed | 8673-8681 | 1 |  |  |  |
| 201 | `drawBaselineMarker` | engine | 8683-8697 | 0 |  |  |  |
| 202 | `drawReplayCursor` | engine | 8699-8713 | 0 |  |  |  |
| 203 | `renderDeltaLine` | engine | 8715-8729 | 0 |  |  |  |
| 204 | `drawPointLabel` | engine | 8731-8740 | 0 |  |  |  |
| 205 | `drawGridAndAxes` | engine | 8742-8787 | 0 |  |  |  |

## State variables

- `API_BASE` (const, line 1429)
- `SCENARIOS_CATALOGUE` (const, line 1431)
- `MOMENTUM_SCENARIO_IDS` (const, line 1440)
- `ALL_CRITERIA_DATA` (const, line 1441)
- `FAMILY_TOP_FIVE_SCENARIOS` (const, line 1477)
- `TP_SL_SCENARIO_IDS` (const, line 1499)
- `ALL_DATE_DATA` (const, line 1533)
- `LIVE_CHART_CACHE_PREFIX` (const, line 1534)
- `LIVE_CHART_CACHE_TTL_MS` (const, line 1535)
- `LIVE_CHART_CACHE_MAX_BYTES` (const, line 1536)
- `initialLiveDataAvailable` (let, line 1537)
- `liveChartDataLoadedKeys` (const, line 1538)
- `cachedProductsForLive` (let, line 1586)
- `historicalCurveLoads` (const, line 1619)
- `currentReturnType` (let, line 1642)
- `currentCriteria` (let, line 1643)
- `mainScenarioCriteria` (let, line 1644)
- `portfolioCriteria` (let, line 1645)
- `portfolioViewConfigs` (let, line 1646)
- `mainScenarioViewConfig` (let, line 1647)
- `portfolioScenarioConfigs` (let, line 1650)
- `currentProductType` (let, line 1652)
- `currentProduct` (let, line 1654)
- `currentStrategyFamily` (let, line 1655)
- `modelLimit` (let, line 1656)
- `portfolios` (let, line 1657)
- `livePortfolioStore` (let, line 1658)
- `livePortfolioActiveModels` (const, line 1659)
- `overlayRuleLibrary` (let, line 1660)
- `assignedOverlayTradeCache` (const, line 1661)
- `assignedOverlayTradeRequests` (const, line 1662)
- `useAssignedOverlayRule` (let, line 1663)
- `overlayRuleLibraryRequest` (let, line 1664)
- `pendingNamedOverlayRuleConfig` (let, line 1665)
- `editingNamedOverlayRuleId` (let, line 1666)
- `activePortfolioName` (let, line 1667)
- `liveModePriorChartLock` (let, line 1668)
- `liveModeRequestInFlight` (let, line 1669)
- `liveModeStatusMessages` (let, line 1670)
- `portfolioModels` (let, line 1671)
- `pendingFilterDataRefresh` (let, line 1672)
- `lastChartFallbackModels` (let, line 1673)
- `lastChartFallbackContext` (let, line 1674)
- `PORTFOLIO_VIEW_CACHE` (const, line 1677)
- `PORTFOLIO_VIEW_CACHE_MAX` (const, line 1678)
- `PORTFOLIO_VIEW_CACHE_STORAGE_KEY` (const, line 1679)
- `PORTFOLIO_VIEW_PERSIST_MAX` (const, line 1680)
- `PORTFOLIO_VIEW_REQUESTS` (const, line 1681)
- `persistedPortfolioViewCache` (let, line 1682)
- `PORTFOLIO_LAST_VIEW_CACHE` (const, line 1683)
- `portfolioTargetModel` (let, line 1684)
- `portfolioMergeSelection` (const, line 1685)
- `similarStrategyPayload` (let, line 1686)
- `strategyCatalogue` (let, line 1687)
- `strategyCatalogueDate` (let, line 1688)
- `displayTheme` (let, line 1689)
- `liveRefreshSequence` (let, line 1690)
- `liveRefreshTimer` (let, line 1691)
- `liveRefreshIntervalMs` (let, line 1692)
- `portfolioViewRefreshTimer` (let, line 1693)
- `portfolioViewRefreshInFlight` (let, line 1694)
- `PORTFOLIO_VIEW_REFRESH_MS` (const, line 1697)
- `currentDate` (let, line 1700)
- `splitMode` (let, line 1701)
- `modelSearchLoadedModels` (let, line 1703)
- `pinnedComparisonModels` (const, line 1704)
- `modelSearchRequestSequence` (let, line 1705)
- `modelSearchTimer` (let, line 1706)
- `deepLinkModel` (let, line 1707)
- `deepLinkModels` (let, line 1708)
- `deepLinkModelsOnly` (let, line 1709)
- `deepLinkDate` (let, line 1710)
- `selectedModelIndex` (let, line 1711)
- `baselineFrameIndex` (let, line 1712)
- `currentFrameIndex` (let, line 1713)
- `minWinRate` (let, line 1714)
- `visibleModels` (let, line 1715)
- `scenarioRemovedModels` (const, line 1718)
- `POINT_IN_TIME_SELECTION_STORAGE_KEY` (const, line 1719)
- `SELECTED_TIME_RANK_STORAGE_KEY` (const, line 1720)
- `pointInTimeSelectionPreference` (let, line 1721)
- `pointInTimeMode` (let, line 1722)
- `top1AtTimePreviousPointInTimeMode` (let, line 1723)
- `pointInTimeModels` (let, line 1724)
- `pointInTimeTimelineModels` (let, line 1728)
- `pointInTimeRequestSequence` (let, line 1729)
- `pointInTimeRequestedKey` (let, line 1730)
- `pointInTimeDebounceTimer` (let, line 1731)
- `pointInTimeHours` (let, line 1732)
- `pointInTimeHistoryKey` (let, line 1733)
- `pointInTimeHistorySequence` (let, line 1734)
- `pointInTimeHistoryAt` (let, line 1735)
- `pendingExplicitTop1Time` (let, line 1736)
- `selectedTimeLeaderHistory` (const, line 1737)
- `selectedTimeLeaderHistoryContext` (let, line 1738)
- `selectedTimeExplicitRefresh` (let, line 1739)
- `autoRefreshTop1Enabled` (let, line 1740)
- `autoRefreshTop1Minutes` (let, line 1741)
- `autoRefreshTop1Direction` (let, line 1742)
- `autoRefreshTop1Rank` (let, line 1743)
- `autoRefreshTop1LastMinute` (let, line 1744)
- `autoRefreshTop1NextMinute` (let, line 1745)
- `autoRefreshTop1Context` (let, line 1746)
- `autoRefreshTop1RequestAt` (let, line 1747)
- `showNetDelta` (let, line 1750)
- `showBuyDelta` (let, line 1751)
- `showSellDelta` (let, line 1752)
- `showTradeMarkers` (let, line 1753)
- `showTradeValues` (let, line 1754)
- `lastOverlayTrades` (let, line 1755)
- `exitThreshold` (let, line 1756)
- `overlayTopX` (let, line 1757)
- `dailyTarget` (let, line 1758)
- `hourlyReportFamily` (let, line 1759)
- `hourlyReportDate` (let, line 1760)
- `hourlyReportTimer` (let, line 1761)
- `hourlyReportRequest` (let, line 1762)
- `hourlyReportPayload` (let, line 1763)
- `hourlyReportInterval` (let, line 1764)
- `chartLocked` (let, line 1768)
- `isPlaying` (let, line 1773)
- `replayInterval` (let, line 1774)
- `replaySpeed` (let, line 1775)
- `BASE_INTERVAL_MS` (const, line 1776)
- `returnTypeNetBtn` (const, line 1792)
- `returnTypeAltBtn` (const, line 1793)
- `openScenarioModalBtn` (const, line 1794)
- `closeScenarioModalBtn` (const, line 1795)
- `closeScenarioModalFooterBtn` (const, line 1796)
- `scenarioModal` (const, line 1797)
- `modalScenarioCards` (const, line 1798)
- `scenarioSearchInput` (const, line 1799)
- `activeScenarioIcon` (const, line 1800)
- `activeScenarioName` (const, line 1801)
- `activeCriteriaLabel` (const, line 1802)
- `dateTabsContainer` (const, line 1804)
- `productTypeFilter` (const, line 1805)
- `productFilter` (const, line 1806)
- `strategyFamilyFilter` (const, line 1807)
- `modelLimitFilter` (const, line 1808)
- `modelSearchInput` (const, line 1809)
- `modelSearchStatus` (const, line 1810)
- `portfolioTabs` (const, line 1811)
- `portfolioModal` (const, line 1812)
- `savePortfolioWorkspaceBtn` (const, line 1813)
- `portfolioWorkspaceSaveStatus` (const, line 1814)
- `overlayRuleLibraryModal` (const, line 1815)
- `overlayRuleNameModal` (const, line 1816)
- `liveRuleStatus` (const, line 1817)
- `livePortfolioTransitionBanner` (const, line 1818)
- `portfolioList` (const, line 1819)
- `mergePortfolioForm` (const, line 1820)
- `mergePortfolioBtn` (const, line 1821)
- `mergePortfolioSummary` (const, line 1822)
- `mergePortfolioCount` (const, line 1823)
- `selectAllPortfoliosBtn` (const, line 1824)
- `deleteSelectedPortfoliosBtn` (const, line 1825)
- `strategyCataloguePanel` (const, line 1826)
- `strategyCatalogueResults` (const, line 1827)
- `catalogPortfolioFilter` (const, line 1828)
- `catalogTypeFilter` (const, line 1829)
- `catalogProductFilter` (const, line 1830)
- `catalogFamilyFilter` (const, line 1831)
- `catalogWindowFilter` (const, line 1832)
- `catalogTpFilter` (const, line 1833)
- `catalogSlFilter` (const, line 1834)
- `similarStrategyModal` (const, line 1835)
- `similarStrategyContext` (const, line 1836)
- `similarStrategyOptions` (const, line 1837)
- `themeToggle` (const, line 1838)
- `openHourlyReportBtn` (const, line 1839)
- `hourlyReportModal` (const, line 1840)
- `hourlyProductType` (const, line 1841)
- `hourlyProduct` (const, line 1842)
- `hourlyInterval` (const, line 1843)
- `hourlyFamilyTabs` (const, line 1844)
- `hourlyReportHead` (const, line 1845)
- `hourlyReportBody` (const, line 1846)
- `hourlyReportSummary` (const, line 1847)
- `hourlyColumnToggle` (const, line 1848)
- `hourlyColumnPanel` (const, line 1849)
- `activeDateLabel` (const, line 1850)
- `winRateDisplayBadge` (const, line 1851)
- `replayStartBadge` (const, line 1852)
- `cardsGridTitle` (const, line 1853)
- `canvas` (const, line 1854)
- `ctx` (const, line 1855)
- `tooltip` (const, line 1856)
- `modelCardsContainer` (const, line 1857)
- `metricAll` (const, line 1859)
- `metricBuy` (const, line 1860)
- `metricSell` (const, line 1861)
- `metricTriSplit` (const, line 1862)
- `metricMultiSplit` (const, line 1863)
- `showAllBtn` (const, line 1865)
- `hideAllBtn` (const, line 1866)
- `clearHiddenBtn` (const, line 1867)
- `clearAllStrategiesBtn` (const, line 1868)
- `playBtn` (const, line 1871)
- `playIcon` (const, line 1872)
- `playBtnText` (const, line 1873)
- `stepBackBtn` (const, line 1874)
- `stepFwdBtn` (const, line 1875)
- `restartBtn` (const, line 1876)
- `speed1x` (const, line 1877)
- `speed025x` (const, line 1878)
- `speed05x` (const, line 1879)
- `speed3x` (const, line 1880)
- `speed10x` (const, line 1881)
- `replayTimeBadge` (const, line 1883)
- `replayProgressPercent` (const, line 1884)
- `baselineTimeBadge` (const, line 1885)
- `selectedTimeForm` (const, line 1886)
- `selectedTimeRankSelect` (const, line 1887)
- `selectedTimeInput` (const, line 1888)
- `applySelectedTimeBtn` (const, line 1889)
- `autoRefreshTop1Toggle` (const, line 1890)
- `autoRefreshTop1Interval` (const, line 1891)
- `autoRefreshTop1DirectionSelect` (const, line 1892)
- `autoRefreshTop1RankSelect` (const, line 1893)
- `autoRefreshTop1Status` (const, line 1894)
- `savedSelectedTimeRank` (const, line 1895)
- `setBaseAtHeadBtn` (const, line 1916)
- `resetBaselineBtn` (const, line 1917)
- `chartLockBtn` (const, line 1918)
- `chartLockIcon` (const, line 1919)
- `chartLockLabel` (const, line 1920)
- `liveModeBtn` (const, line 1921)
- `liveModeLabel` (const, line 1922)
- `scrubberTrack` (const, line 1924)
- `scrubberFill` (const, line 1925)
- `scrubberThumb` (const, line 1926)
- `baselineMarker` (const, line 1927)
- `baselineBadge` (const, line 1928)
- `winRateSlider` (const, line 1930)
- `winRateValBadge` (const, line 1931)
- `toggleNetDeltaBtn` (const, line 1934)
- `pointInTimeToggle` (const, line 1935)
- `pointInTimeStatus` (const, line 1936)
- `pointInTimeHistoryPanel` (const, line 2048)
- `pointInTimeHistoryStatus` (const, line 2049)
- `pointInTimeHistoryRows` (const, line 2050)
- `pointInTimeHistoryNearViewport` (let, line 2051)
- `toggleBuyDeltaBtn` (const, line 2061)
- `toggleSellDeltaBtn` (const, line 2062)
- `netDeltaCheck` (const, line 2063)
- `buyDeltaCheck` (const, line 2064)
- `sellDeltaCheck` (const, line 2065)
- `toggleTradeMarkersBtn` (const, line 2066)
- `tradeMarkersCheck` (const, line 2067)
- `ribbonModelName` (const, line 2069)
- `ribbonProduct` (const, line 2070)
- `ribbonStrategy` (const, line 2071)
- `ribbonTotNet` (const, line 2072)
- `ribbonBuyNet` (const, line 2073)
- `ribbonSellNet` (const, line 2074)
- `totalNetLabel` (const, line 2075)
- `buyNetLabel` (const, line 2076)
- `sellNetLabel` (const, line 2077)
- `indicatorBar` (const, line 2078)
- `portfolioWorkspaceStorageKeys` (const, line 2228)
- `liveActivationModal` (const, line 3122)
- `liveActivationForm` (const, line 3123)
- `liveActivationRule` (const, line 3124)
- `LIVE_REFRESH_MS` (const, line 4634)
- `LIVE_MODE_REFRESH_MS` (const, line 4635)
- `HOURLY_REPORT_FAMILIES` (const, line 6423)
- `HOURLY_COLUMN_PREF_KEY` (const, line 6428)
- `HOURLY_METRICS` (const, line 6429)
- `HOURLY_COLUMNS` (const, line 6435)
- `hourlyVisibleColumns` (let, line 6445)
- `timeAxisPoints` (let, line 7570)
- `dashboardUtilityRuntimeScheduled` (let, line 8672)
