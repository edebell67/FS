"""Chronological holdout calibration proof for regime direction confidence."""
from __future__ import annotations
from datetime import datetime,timezone
import json,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from app.intelligence.regime import CALIBRATED_DIRECTION_PERSISTENCE,CALIBRATION_VERSION,classify


def main():
    rows=json.loads((ROOT/"runtime"/"market_features.json").read_text(encoding="utf-8"))["features"];observations=[]
    for current,nxt in zip(rows,rows[1:]):
        prediction=classify(current["features"]);actual=classify(nxt["features"])["direction"]
        bin_index=min(4,max(0,int((prediction["model_margin"]-.5)/.1)));observations.append({"bin":bin_index,"correct":prediction["direction"]==actual,"as_of":current["as_of"]})
    split=int(len(observations)*.8);calibration=observations[:split];holdout=observations[split:]
    fitted={index:(sum(item["correct"] for item in calibration if item["bin"]==index)+1)/(sum(item["bin"]==index for item in calibration)+2) for index in range(5)}
    mapping_matches=all(abs(fitted[index]-CALIBRATED_DIRECTION_PERSISTENCE[index])<1e-9 for index in range(5));ece=sum(abs(fitted[item["bin"]]-float(item["correct"])) for item in holdout)/len(holdout)
    checks={"chronological_split":calibration[-1]["as_of"]<holdout[0]["as_of"],"deployed_mapping_matches_calibration_partition":mapping_matches,"holdout_observations_at_least_50":len(holdout)>=50,"holdout_mean_absolute_calibration_error_below_0_10":ece<.1}
    report={"schema_version":"1.0.0","generated_at":datetime.now(timezone.utc).isoformat(),"calibration_version":CALIBRATION_VERSION,"target":"next-observation direction persistence","method":"0.10-wide model-margin bins with Laplace smoothing, fitted on first 80% and evaluated on final 20% chronologically","passed":all(checks.values()),"checks":checks,"calibration_observations":len(calibration),"holdout_observations":len(holdout),"holdout_accuracy":sum(item["correct"] for item in holdout)/len(holdout),"holdout_mean_absolute_calibration_error":ece,"fitted_mapping":fitted,"limitations":["Confidence measures next-observation direction persistence, not forecast return or profitability.","Daily ECB reference observations are informational and not executable prices."]}
    target=ROOT/"evidence"/"regime_confidence_calibration_report.json";target.write_text(json.dumps(report,indent=2),encoding="utf-8");print(json.dumps(report))


if __name__=="__main__":main()
