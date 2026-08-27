"""Operator-run full local profile warm-up; public requests never trigger the expensive series scan."""
from datetime import datetime,timezone
import json
from pathlib import Path
from app.config import get_settings
from app.intelligence.comparative import score_profile
from app.intelligence.profile import build_profile
from app.intelligence.cache import SCHEMA_VERSION,cache_hash
from app.repository import local_equity_curves,local_strategies


def main():
    settings=get_settings();summaries=local_strategies(settings);summaries.sort(key=lambda item:(-item["total_trades"],item["strategy_id"]));summaries=summaries[:settings.intelligence_catalog_limit];curves=local_equity_curves(settings,[item["strategy_id"] for item in summaries]);profiles=[]
    for summary in summaries:
        profile=build_profile(summary,curves.get(summary["strategy_id"],[])).model_dump(mode="json");profile["score"]=score_profile(profile);profiles.append(profile)
    payload={"schema_version":SCHEMA_VERSION,"generated_at":datetime.now(timezone.utc).isoformat(),"catalog_size":len(profiles),"profile_depth":"full","summaries":summaries,"profiles":profiles,"curves":curves};payload["sha256"]=cache_hash(payload)
    target=Path(settings.local_intelligence_cache_path);target=target if target.is_absolute() else Path(__file__).resolve().parents[1]/target;target.parent.mkdir(parents=True,exist_ok=True);temporary=target.with_suffix(".tmp");temporary.write_text(json.dumps(payload,separators=(",",":")),encoding="utf-8");temporary.replace(target);print(json.dumps({"cache":str(target),"profiles":len(profiles),"points":sum(map(len,curves.values()))}))


if __name__=="__main__":main()
