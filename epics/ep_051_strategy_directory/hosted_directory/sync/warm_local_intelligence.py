"""Operator-run full local profile warm-up; public requests never trigger the expensive series scan.

Version history:
- 1.1.0 (2026-08-30): Adds --interval/--once loop mode (mirrors
  scripts/refresh_directory_summary_cache.py's pattern) so this can run
  supervised under _one_run_single.ps1 instead of only via a manual
  one-shot command - AUTO-04/LOC-02's actual blocker. No restart needed
  to pick up fresh output: app/main.py's local_snapshot() already
  re-reads this file on mtime change, live.
- 1.0.0: Original one-shot warm-up script.
"""
import argparse,time
from datetime import datetime,timezone
import json
from pathlib import Path
from app.config import get_settings
from app.intelligence.comparative import score_profile
from app.intelligence.profile import build_profile
from app.intelligence.cache import SCHEMA_VERSION,cache_hash
from app.repository import local_equity_curves,local_strategies


def refresh():
    settings=get_settings();summaries=local_strategies(settings);summaries.sort(key=lambda item:(-item["total_trades"],item["strategy_id"]));summaries=summaries[:settings.intelligence_catalog_limit];curves=local_equity_curves(settings,[item["strategy_id"] for item in summaries]);profiles=[]
    for summary in summaries:
        profile=build_profile(summary,curves.get(summary["strategy_id"],[])).model_dump(mode="json");profile["score"]=score_profile(profile);profiles.append(profile)
    payload={"schema_version":SCHEMA_VERSION,"generated_at":datetime.now(timezone.utc).isoformat(),"catalog_size":len(profiles),"profile_depth":"full","summaries":summaries,"profiles":profiles,"curves":curves};payload["sha256"]=cache_hash(payload)
    target=Path(settings.local_intelligence_cache_path);target=target if target.is_absolute() else Path(__file__).resolve().parents[1]/target;target.parent.mkdir(parents=True,exist_ok=True);temporary=target.with_suffix(".tmp");temporary.write_text(json.dumps(payload,separators=(",",":")),encoding="utf-8");temporary.replace(target);print(json.dumps({"cache":str(target),"profiles":len(profiles),"points":sum(map(len,curves.values()))}),flush=True)


def main():
    parser=argparse.ArgumentParser();parser.add_argument("--interval",type=int,default=10800);parser.add_argument("--once",action="store_true");args=parser.parse_args()
    while True:
        try:refresh()
        except Exception as exc:print(f"intelligence warm-up failed: {exc}",flush=True)
        if args.once:return
        time.sleep(max(300,args.interval))


if __name__=="__main__":main()
