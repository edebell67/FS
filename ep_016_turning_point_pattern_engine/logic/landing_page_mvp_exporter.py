import json
import os
from datetime import datetime

# Path to the full stat pack
SOURCE_JSON = r"C:\Users\edebe\eds\epics\ep_016_turning_point_pattern_engine\outputs\ep016_marketing_stats_pack.json"
OUTPUT_JSON = r"C:\Users\edebe\eds\epics\ep_016_turning_point_pattern_engine\outputs\ep016_landing_page_mvp.json"

def generate_mvp_subset():
    if not os.path.exists(SOURCE_JSON):
        print(f"Error: Source {SOURCE_JSON} not found.")
        return

    with open(SOURCE_JSON, "r", encoding="utf-8") as f:
        full = json.load(f)

    # Extract strictly LIVE high-impact metrics
    mvp = {
        "metadata": {
            "status": "LIVE_MARKET_MONITORING",
            "last_update": full["engine_health"]["last_snapshot_time"],
            "engine_freshness_seconds": full["engine_health"]["data_freshness_seconds"],
            "verified_sample_size": full["live_performance_claims"]["verified_sample_size"]
        },
        "headline_stats": {
            "total_patterns_detected": full["live_detection"]["total_live_turns_detected"],
            "markets_under_monitoring": full["engine_health"]["active_monitored_products"],
            "structural_stability_rate": f"{full['live_performance_claims']['structural_stability_10m_pct']}%",
            "avg_move_captured_pips": full["live_performance_claims"]["avg_move_captured_pips"]
        },
        "engine_quality": {
            "avg_confirmation_delay": f"{full['live_quality']['avg_confirm_delay_minutes']} min",
            "structural_quality_score": full["live_quality"]["avg_structural_quality_score"],
            "market_coverage": f"{full['live_coverage']['market_coverage_pct']}%"
        }
    }

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(mvp, f, indent=2)

    print(f"LIVE MVP Landing Page stats saved to: {OUTPUT_JSON}")

if __name__ == "__main__":
    generate_mvp_subset()
