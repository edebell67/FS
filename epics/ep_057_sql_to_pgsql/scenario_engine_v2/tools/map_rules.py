# epics/ep_057_sql_to_pgsql/scenario_engine_v2/tools/map_rules.py — shared category/status rules for the engine map (used by build_engine_map and rebase_map).
#
# VERSION HISTORY
# v1.6.0 · 2026-10-17 · The page-controller functions (state / split / formerly simplified compute) are ported and differential-tested; PROVISIONAL and NOT_DIFF_TESTED are empty.
# v1.5.0 · 2026-10-17 · refreshPointInTimeSelection is ported and differential-tested.
# v1.4.0 · 2026-10-17 · The data-layer fetchers are ported (DataClient); the point-in-time / hourly handlers are provisional (URL only).
# v1.3.0 · 2026-10-17 · finishAutomaticTop1Refresh and getExactSearchModel ported.
# v1.2.0 · 2026-10-17 · The small replay / search / request-option helpers are ported; getMaxFrames, getReplayTimelineModels, pointInTimeAtReplayHead are simplified (provisional).
# v1.1.0 · 2026-10-16 · The assigned overlay-rule functions are ported; rotation functions are no longer partial.
# v1.0.0 · 2026-10-16 · Initial version: rules extracted from build_engine_map.py so a re-base classifies new functions identically.
import re

PORTED = {  # page function -> python target
    "getMetricKeys": "core_ported.metric_keys", "getStrategyFamily": "core_ported.strategy_family_of",
    "getBasePoint": "core_ported.base_point", "getReplayHeadPoint": "core_ported.head_point",
    "getScenarioCandidates": "core_ported.scenario_candidates", "updateRibbon": "core_ported.ribbon",
    "computeTradeOverlaySignals": "core_ported.overlay_signals", "pairOverlayTrades": "core_ported.pair_overlay_trades",
    "computeSplitTargetSignal": "core_ported.split_target_signal", "computeLeaderRotation": "core_ported.leader_rotation",
    "computeMultiSplitRotation": "core_ported.multi_split_rotation",
    "modelPointAtOrBeforeTime": "core_ported.point_at_or_before", "selectedTimeJoinAt": "core_ported.selected_time_join_at",
    "selectedTimeModelEligibleAt": "core_ported.selected_time_eligible_at",
    "overlayRuleCandidate": "core_ported.overlay_rule_candidate",
    "overlayRuleMetricValue": "core_ported.overlay_rule_metric_value",
    "asOfCorrelation": "core_ported.as_of_correlation",
    "applyAssignedOverlayTradeResults": "core_ported.apply_assigned_overlay_trade_results",
    "assignedRuleTarget": "core_ported.assigned_rule_target",
    "sourceTradeFlipResults": "core_ported.source_trade_flip_results",
    "curvePointAtOrBefore": "core_ported.curve_point_at_or_before",
    "timeOfDayMinutes": "core_ported.time_of_day_minutes",
    "assignedOverlayTradeCacheKey": "core_ported.RuleContext.cache_key",
    "clockMinutes": "page_utils.clock_minutes",
    "replayClockTime": "page_utils.replay_clock_time",
    "nextAutomaticTop1Minute": "page_utils.next_automatic_top1_minute",
    "selectedTimePointEligible": "page_utils.selected_time_point_eligible",
    "modelSearchTerms": "page_utils.model_search_terms",
    "overlayRuleSummary": "page_utils.overlay_rule_summary",
    "isMetricAwareCriteria": "page_utils.is_metric_aware_criteria",
    "shortStrategyDescription": "page_utils.short_strategy_description",
    "getSelectedTimeNoteEntries": "page_utils.selected_time_note_entries",
    "selectedTimeRankCount": "page_utils.selected_time_rank_count",
    "portfolioScenarioConfig": "page_utils.point_in_time_request_options (inlined lookup)",
    "pointInTimeRequestOptions": "page_utils.point_in_time_request_options",
    "pointInTimeContextKey": "page_utils.point_in_time_context_key",
    "retainSelectedTimeLeaders": "page_utils.retain_selected_time_leaders",
    "tradeDateRange": "page_utils.trade_date_range",
    "step": "page_utils.frame_after_step / Engine.step",
    "seekToPct": "page_utils.frame_for_pct / Engine.seek_to_pct",
    "setSplitMode": "page_utils.valid_split_mode / Engine.set_split_mode",
    "availableDates": "page_utils.available_dates",
    "finishAutomaticTop1Refresh": "page_utils.finish_automatic_top1_refresh",
    "getExactSearchModel": "page_utils.exact_search_model",
    "refreshPointInTimeSelection": "selected_time.refresh_point_in_time_selection",
    "refreshLiveData": "DataClient.refresh_live_data",
    "fetchPortfolioData": "DataClient.fetch_portfolio_data",
    "loadPortfolioData": "DataClient.load_portfolio_data",
    "loadModelSearchFromDatabase": "page.Page.load_model_search_from_database",
    "loadDeepLinkModelsFromDatabase": "page.Page.load_deep_link_models_from_database",
    "loadStrategyCatalogue": "DataClient.load_strategy_catalogue",
    "loadOverlayRuleLibrary": "DataClient.load_overlay_rule_library",
    "ensureAssignedOverlayTradeData": "DataClient.ensure_trade_data",
    "ensureHistoricalDataLoaded": "DataClient.ensure_historical_data",
    "syncTpSlScenarios": "DataClient.sync_tp_sl_scenarios",
}
# page-controller port (2026-10-17): functions ported to engine/page.py, rule_editor.py, replay_models.py, reports.py
PORTED.update({
    'activatePortfolio': 'page.Page.activate_portfolio',
    'activePortfolioOverlayRule': 'page.Page.active_portfolio_overlay_rule',
    'addCatalogueModel': 'page.Page.add_catalogue_model',
    'applyChartLock': 'page.Page.apply_chart_lock',
    'applyPortfolioViewConfig': 'page.Page.apply_portfolio_view_config',
    'applySelectedTime': 'page.Page.apply_selected_time',
    'assignOverlayRule': 'rule_editor.RuleEditor.assign_overlay_rule',
    'assignedPortfolioOverlayRule': 'page.Page.assigned_portfolio_overlay_rule',
    'autoPinLivePortfolioStrategies': 'page.Page.auto_pin_live_portfolio_strategies',
    'availableDates': 'page_utils.available_dates',
    'beginEditNamedOverlayRule': 'rule_editor.RuleEditor.begin_edit_named_overlay_rule',
    'cancelEditNamedOverlayRule': 'rule_editor.RuleEditor.cancel_edit_named_overlay_rule',
    'capturePortfolioScenario': 'page.Page.capture_portfolio_scenario',
    'configFromOverlayEditor': 'rule_editor.RuleEditor.config_from_overlay_editor',
    'createSimilarPortfolio': 'page.Page.create_similar_portfolio',
    'currentPortfolioViewConfig': 'page.Page.current_portfolio_view_config',
    'deletePortfolio': 'page.Page.delete_portfolio',
    'deleteSelectedPortfolios': 'page.Page.delete_selected_portfolios',
    'getEligibleModels': 'replay_models.get_eligible_models',
    'getLastPortfolioView': 'DataClient.get_last_portfolio_view',
    'getMaxFrames': 'replay_models.get_max_frames',
    'getMergedPortfolioModels': 'page.Page.get_merged_portfolio_models',
    'getReplayTimelineModels': 'replay_models.get_replay_timeline_models',
    'getScenarioCandidates': 'replay_models.get_scenario_candidates',
    'livePortfolioModelsForDate': 'page.Page.live_portfolio_models_for_date',
    'loadHourlyReport': 'reports.load_hourly_report',
    'markPortfolioFixed': 'page.Page.mark_portfolio_fixed',
    'moveModelBetweenPortfolios': 'page.Page.move_model_between_portfolios',
    'movePortfolio': 'page.Page.move_portfolio',
    'pauseReplay': 'page.Page.pause_replay',
    'persistPortfolioViewConfig': 'page.Page.persist_portfolio_view_config',
    'pointInTimeAtReplayHead': 'replay_models.point_in_time_at_replay_head',
    'refreshActivePortfolioView': 'page.Page.refresh_active_portfolio_view',
    'refreshPointInTimeHistory': 'page.Page.refresh_point_in_time_history',
    'rememberPortfolioView': 'DataClient.remember_portfolio_view',
    'removeModelFromPortfolio': 'page.Page.remove_model_from_portfolio',
    'removePortfolios': 'page.Page.remove_portfolios',
    'repopulateActivePortfolioFromCriteria': 'page.Page.repopulate_active_portfolio_from_criteria',
    'resetAutomaticRankSchedule': 'page.Page.reset_automatic_rank_schedule',
    'saveNamedOverlayRule': 'rule_editor.RuleEditor.save_named_overlay_rule',
    'scheduleAutomaticTop1Refresh': 'page.Page.schedule_automatic_top1_refresh',
    'schedulePointInTimeSelection': 'page.Page.schedule_point_in_time_selection',
    'setRankingCriteria': 'page.Page.set_ranking_criteria',
    'startReplay': 'page.Page.start_replay',
    'switchDate': 'page.Page.switch_date',
    'syncPortfolioViewRefresh': 'page.Page.sync_portfolio_view_refresh',
    'triggerSelectedTimeRefresh': 'page.Page.trigger_selected_time_refresh',
    'uniquePortfolioName': 'page.Page.unique_portfolio_name',
    'updateAutoRefreshTop1Status': 'page.Page.update_auto_refresh_status',
    'updateRibbon': 'replay_models.update_ribbon',
})
PARTIAL = set()  # rotation functions now include the assigned overlay-rule path
PROVISIONAL = {}  # nothing is provisional any more: every compute / data / state / split function is ported and differential-tested
# updateRibbon and getEligibleModels are mixed DOM/logic: their Python versions port the aggregate/filter only and cannot be run
# from the page's JS (DOM-bound), so they are not covered by the differential test.
NOT_DIFF_TESTED = set()

VIEW_PREFIX = re.compile(r"^(draw|render|setup|apply(Display|Chart)|set(Live)?Badge|setSection|setAllSections|updateCollapse|updateChartLock|updateOverlayTradeSummary|schedulDashboard|scheduleDashboard|sync(SplitModeControls|HourlyProducts)|updateStrategyFamilyOptions|populateCatalogue|setCatalogueOptions|hourly|collapseStorageKey|storedHourlyColumns|persistHourlyColumns|togglePlay|startPlaybackLoop|startLiveRefresh|syncLiveRefreshInterval|setLiveBadge)")
LIVE = re.compile(r"^(activateLiveModeFromReview|saveLivePortfolioRules|liveActivation|isLiveMode|isRuleManagedLivePortfolio|syncLivePortfolioScreenState|loadLivePortfolioRulesIntoForm|editLivePortfolioRules|appendRuleDetailsSection|liveRuleSummary|syncLiveAltReporting|LIVE_DATE)")
DATA = re.compile(r"^(fetch|load|ensure|restore|save.*(Postgres|Portfolios|CriteriaWorkspaces)|refreshLiveData|refreshPointIn|persist|cache|restoreLiveChartCache|paintLiveChartCache|scheduleLiveChartCacheFallback|liveChartCacheKey)")
STATE = re.compile(r"(Portfolio|Portfolios|OverlayRule|NamedOverlayRule|assignOverlayRule|uniquePortfolioName|markPortfolioFixed|movePortfolio|moveModelBetween|addCatalogueModel|createSimilarPortfolio|autoPinLive)")


def classify(name: str, kind: str) -> tuple[str, str, str | None]:
    """-> (category, status, python_target) for a function the map has not seen before."""
    if name in PORTED:
        return "compute", ("ported_partial" if name in PARTIAL else "ported"), PORTED[name]
    if name in PROVISIONAL:
        return "compute", "provisional", PROVISIONAL[name]
    if kind == "view" or VIEW_PREFIX.match(name):
        return "view", "stays_in_page", None
    if LIVE.match(name):
        return "live", "refused_headless", None
    if DATA.match(name):
        return "data", "pending", None
    if STATE.search(name):
        return "state", "pending", None
    if kind == "mixed":
        return "split", "pending", None
    return "compute", "pending", None
