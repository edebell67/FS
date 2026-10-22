"""Repeatability and protected-slice evaluation for deterministic discovery."""
from __future__ import annotations
from datetime import datetime,timezone
import json,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from app.intelligence.discovery import interpret,retrieve


def main():
    corpus=json.loads((ROOT/"assurance"/"discovery_corpus.json").read_text(encoding="utf-8"));profiles=json.loads((ROOT/"runtime"/"intelligence_profiles.json").read_text(encoding="utf-8"))["profiles"]
    runs=[]
    for repeat in range(10):runs.append([{"id":case["id"],"plan":interpret(case["query"]).model_dump(mode="json",exclude_none=True)} for case in corpus])
    stable=all(run==runs[0] for run in runs[1:]);exact=all(item["plan"]==next(case["expected"] for case in corpus if case["id"]==item["id"]) for item in runs[0])
    slices=[]
    for case in corpus:
        plan=interpret(case["query"]);items=retrieve(profiles,plan);hard_valid=all((plan.asset_class is None or item["profile"]["classification"]["asset_class"].lower()==plan.asset_class.lower()) and (plan.min_win_rate is None or (item["profile"]["metrics"]["win_rate"]["value"] or 0)>=plan.min_win_rate) for item in items)
        slices.append({"id":case["id"],"result_count":len(items),"hard_constraints_valid":hard_valid,"rank_stable":items==retrieve(profiles,plan)})
    checks={"ten_repeat_plans_identical":stable,"exact_plan_match":exact,"all_protected_slices_enforce_hard_constraints":all(item["hard_constraints_valid"] for item in slices),"all_protected_slices_rank_repeatably":all(item["rank_stable"] for item in slices)}
    report={"schema_version":"1.0.0","generated_at":datetime.now(timezone.utc).isoformat(),"passed":all(checks.values()),"checks":checks,"repeat_runs":10,"cases":len(corpus),"protected_slices":slices}
    target=ROOT/"evidence"/"discovery_ranking_variance_report.json";target.write_text(json.dumps(report,indent=2),encoding="utf-8");print(json.dumps(report))


if __name__=="__main__":main()
