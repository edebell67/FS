"""Public launch decision gate. Version 1.0.0 (2026-08-23)."""
REQUIRED=("external_beta_passed","production_slo_passed","data_quality_stable","rollback_proven","security_approved","analytics_approved","operations_approved")
def decide(evidence):
 missing=[key for key in REQUIRED if evidence.get(key) is not True]
 return {"decision":"GO" if not missing else "NO_GO","missing":missing,"staged_traffic":[1,5,25,50,100],"automatic_rollback_on":["error_budget","stale_data","quality_failure","security_incident"]}

