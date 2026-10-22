"""Strategy lifecycle governance. Version 1.0.0 (2026-08-23)."""
from datetime import datetime, timezone

TRANSITIONS={
"collecting":{"eligible","quarantined","retired"},"eligible":{"active","quarantined","retired"},
"active":{"paused","quarantined","retired"},"paused":{"active","quarantined","retired"},
"quarantined":{"collecting","retired"},"retired":set()}
PRIVILEGED={"operator","admin"}

def transition(record,to_state,*,principal,reason,evidence_id):
    if principal.get("role") not in PRIVILEGED: raise PermissionError("operator approval required")
    current=record["state"]
    if to_state not in TRANSITIONS[current]: raise ValueError("invalid transition")
    if not reason or not evidence_id: raise ValueError("reason and evidence required")
    history=list(record.get("history",[]));history.append({"from":current,"to":to_state,"actor":principal["subject"],"reason":reason,"evidence_id":evidence_id,"at":datetime.now(timezone.utc).isoformat()})
    return {**record,"state":to_state,"deployment_eligible":to_state=="active","history":history}

def evaluate_flags(*,data_age_seconds,age_limit_seconds,observed_drift,drift_limit,definition_version,required_definition_version):
    flags=[]
    if data_age_seconds>age_limit_seconds:flags.append("STALE")
    if abs(observed_drift)>drift_limit:flags.append("DRIFT")
    if definition_version!=required_definition_version:flags.append("DEFINITION_MISMATCH")
    return flags

