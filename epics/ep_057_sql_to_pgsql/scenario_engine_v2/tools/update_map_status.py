# epics/ep_057_sql_to_pgsql/scenario_engine_v2/tools/update_map_status.py — records the page-controller port in the engine map (state / split rows -> ported, simplified rows -> ported + differential-tested).
#
# VERSION HISTORY
# v1.2.0 · 2026-10-17 · drawChart note: the engine-relevant decisions it embeds.
# v1.1.0 · 2026-10-17 · refreshPointInTimeHistory and loadHourlyReport.
# v1.0.0 · 2026-10-17 · Initial version: updates engine_map_v2.65.32.json in place (statuses, python targets, verified hashes, notes) and prints the summary; refuses names that are not in the map.
"""python update_map_status.py [engine_map.json]. Only rows listed below change; everything else is left exactly as it was."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAP = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "engine_map_v2.65.32.json"

P = "page.Page."
# name -> (category, status, python_target, differential_tested, note)
UPDATES = {
    # ---- state: portfolio store, view config, overlay-rule lookups (tools/diff_page_js_vs_py.py)
    "movePortfolio": ("state", "ported", P + "move_portfolio", True, None),
    "currentPortfolioViewConfig": ("state", "ported", P + "current_portfolio_view_config", True, None),
    "applyPortfolioViewConfig": ("state", "ported", P + "apply_portfolio_view_config", True, None),
    "livePortfolioModelsForDate": ("state", "ported", P + "live_portfolio_models_for_date", True, None),
    "autoPinLivePortfolioStrategies": ("state", "ported", P + "auto_pin_live_portfolio_strategies", True, None),
    "assignedPortfolioOverlayRule": ("state", "ported", P + "assigned_portfolio_overlay_rule", True, None),
    "activePortfolioOverlayRule": ("state", "ported", P + "active_portfolio_overlay_rule", True, None),
    "capturePortfolioScenario": ("state", "ported", P + "capture_portfolio_scenario", True, None),
    "markPortfolioFixed": ("state", "ported", P + "mark_portfolio_fixed", True, None),
    "removeModelFromPortfolio": ("state", "ported", P + "remove_model_from_portfolio", True, None),
    "deletePortfolio": ("state", "ported", P + "delete_portfolio", True, "The confirm() dialog is a parameter (confirmed=True)."),
    "deleteSelectedPortfolios": ("state", "ported", P + "delete_selected_portfolios", True, "The confirm() dialog is a parameter (confirmed=True)."),
    "removePortfolios": ("state", "ported", P + "remove_portfolios", True, None),
    "addCatalogueModel": ("state", "ported", P + "add_catalogue_model", True, "The page's alert() on a full portfolio is dropped; the state change is identical."),
    "moveModelBetweenPortfolios": ("state", "ported", P + "move_model_between_portfolios", True, None),
    "getMergedPortfolioModels": ("state", "ported", P + "get_merged_portfolio_models", True, None),
    "refreshActivePortfolioView": ("state", "ported", P + "refresh_active_portfolio_view", True, None),
    "syncPortfolioViewRefresh": ("state", "ported", P + "sync_portfolio_view_refresh", True, None),
    "repopulateActivePortfolioFromCriteria": ("state", "ported", P + "repopulate_active_portfolio_from_criteria", True, None),
    "activatePortfolio": ("state", "ported", P + "activate_portfolio", True, "Ordinary portfolios only: LIVE / LIVE_ALT are refused headless (LivePortfolioRefused)."),
    "uniquePortfolioName": ("state", "ported", P + "unique_portfolio_name", True, None),
    "createSimilarPortfolio": ("state", "ported", P + "create_similar_portfolio", True, None),
    "rememberPortfolioView": ("state", "ported", "DataClient.remember_portfolio_view", True, "In-memory part; the localStorage index is recorded as an effect."),
    "getLastPortfolioView": ("state", "ported", "DataClient.get_last_portfolio_view", True, "In-memory part."),
    "getPersistedPortfolioViewCache": ("state", "not_applicable_headless", None, False,
                                       "Reads localStorage; a headless instance has none (its caches are the in-memory ones)."),
    # ---- overlay-rule editor (tools/diff_rule_editor_js_vs_py.py)
    "beginEditNamedOverlayRule": ("state", "ported", "rule_editor.RuleEditor.begin_edit_named_overlay_rule", True, "The DOM form is one RuleForm object."),
    "cancelEditNamedOverlayRule": ("state", "ported", "rule_editor.RuleEditor.cancel_edit_named_overlay_rule", True, None),
    "saveNamedOverlayRule": ("state", "ported", "rule_editor.RuleEditor.save_named_overlay_rule", True,
                             "Writes go through DataClient.send and are refused unless a write transport is supplied."),
    "assignOverlayRule": ("state", "ported", "rule_editor.RuleEditor.assign_overlay_rule", True,
                          "Writes go through DataClient.send and are refused unless a write transport is supplied."),
    "configFromOverlayEditor": ("split", "ported", "rule_editor.RuleEditor.config_from_overlay_editor", True, None),
    # ---- split: scheduling, replay, navigation (page.Page)
    "triggerSelectedTimeRefresh": ("split", "ported", P + "trigger_selected_time_refresh", True, None),
    "resetAutomaticRankSchedule": ("split", "ported", P + "reset_automatic_rank_schedule", True, None),
    "applySelectedTime": ("split", "ported", P + "apply_selected_time", True, None),
    "scheduleAutomaticTop1Refresh": ("split", "ported", P + "schedule_automatic_top1_refresh", True, None),
    "schedulePointInTimeSelection": ("split", "ported", P + "schedule_point_in_time_selection", True, "Timers are recorded as effects; run_timers() runs them."),
    "switchDate": ("split", "ported", P + "switch_date", True, "Responses apply in issue order; the 'switched away' guards are modelled for the fetched portfolio."),
    "startReplay": ("split", "ported", P + "start_replay", True, "The playback timer is recorded as the startPlaybackLoop effect."),
    "pauseReplay": ("split", "ported", P + "pause_replay", True, None),
    "setRankingCriteria": ("split", "ported", P + "set_ranking_criteria", True, None),
    # ---- were classified 'view' but their state half is ported
    "applyChartLock": ("split", "ported", P + "apply_chart_lock", True, "A live portfolio with armed live mode would force the lock: live mode is refused headless."),
    "persistPortfolioViewConfig": ("split", "ported", P + "persist_portfolio_view_config", True, "localStorage writes are recorded as effects."),
    "updateAutoRefreshTop1Status": ("split", "ported", P + "update_auto_refresh_status", True, None),
    # ---- the formerly simplified compute functions: now faithful and differential-tested (tools/diff_models_js_vs_py.py)
    "getScenarioCandidates": ("compute", "ported", "replay_models.get_scenario_candidates", True,
                              "CORRECTED 2026-10-17: the earlier target core_ported.scenario_candidates was never tested against the page and differed "
                              "(it sorted by return and did not de-duplicate); the page keeps server order and de-duplicates equal rounded returns."),
    "getEligibleModels": ("compute", "ported", "replay_models.get_eligible_models", True, "Includes the model-search status line (state.model_search_status)."),
    "getReplayTimelineModels": ("compute", "ported", "replay_models.get_replay_timeline_models", True, None),
    "pointInTimeAtReplayHead": ("compute", "ported", "replay_models.point_in_time_at_replay_head", True, None),
    "getMaxFrames": ("compute", "ported", "replay_models.get_max_frames", True, None),
    "updateRibbon": ("compute", "ported", "replay_models.update_ribbon", True,
                     "The ribbon's text and colours (TRI_SPLIT selected model, or the visible models' totals); core_ported.ribbon remains the aggregate used by Engine.ribbon()."),
    "refreshPointInTimeHistory": ("data", "ported", P + "refresh_point_in_time_history", True, "The list rendering stays in the page (recorded as the renderPointInTimeHistory effect)."),
    "loadHourlyReport": ("data", "ported", "reports.load_hourly_report", True, "Request + error text only; the report table stays in the page."),
    "availableDates": ("compute", "ported", "page_utils.available_dates", True, "The page's load-time expression run in Node with a fake clock (tools/diff_available_dates.py)."),
    "drawChart": ("view", "stays_in_page", None, False,
                  "Canvas drawing, but it also makes three engine-relevant decisions that the engine does NOT port as one function: (1) the rotation / overlay candidates are the VISIBLE "
                  "models only (Engine.rotation(visible=...) can filter); (2) the split mode picks the function: ALL_NET -> leader rotation, TRI_SPLIT -> per-model overlay of the "
                  "selected model, MULTI_SPLIT -> multi-split rotation (the engine computes all three, the choice is the caller's); (3) drawUpTo clamps the frame to 0..length-1 "
                  "(the engine treats frame -1 as 'latest'). Verified end to end by the browser parity task, not by a differential test."),
}


def main():
    data = json.loads(MAP.read_text(encoding="utf-8"))
    by_name = {}
    for r in data["rows"]:
        by_name.setdefault(r["name"], []).append(r)
    missing = [n for n in UPDATES if n not in by_name]
    if missing:
        sys.exit(f"not in the map: {missing}")
    changed = 0
    for name, (cat, status, target, tested, note) in UPDATES.items():
        for r in by_name[name]:
            r.update({"category": cat, "status": status, "python_target": target, "differential_tested": tested})
            if status in ("ported", "ported_partial"):
                r["verified_body_sha256"] = r["body_sha256"]
            if note:
                r["verification_note"] = note
            else:
                r.pop("verification_note", None)
            changed += 1
    summary = {}
    for r in data["rows"]:
        summary.setdefault(r["category"], {}).setdefault(r["status"], 0)
        summary[r["category"]][r["status"]] += 1
    data["summary"] = summary
    MAP.write_text(json.dumps(data, indent=1), encoding="utf-8")
    print(f"updated {changed} rows in {MAP.name}")
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
