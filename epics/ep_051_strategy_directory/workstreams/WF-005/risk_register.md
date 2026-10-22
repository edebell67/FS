# Risk Register - EP051 DNA Strategy Directory

| Risk ID | Description | Impact | Likelihood | Mitigation Strategy | Owner | Status |
|---|---|---|---|---|---|---|
| R-01 | Unintentional exposure of individual trade GUIDs via public API | High | Low | Implement strict field filtering in the API Gateway. Unit tests to verify payload structure. | Engineering | Open |
| R-02 | Non-DNA trades mixed into DNA aggregates, inflating performance | High | Medium | Enforce `is_dna=true` predicate at the database view level. Alerts on baseline deviations. | Data Team | Mitigated |
| R-03 | Broker API credential leakage | Critical | Low | Broker integration deferred to Phase 6. Vault implementation mandatory before activation. | Security | Deferred |
| R-04 | Malicious internal modification of historical settled trades | High | Low | Database audit logs. Immutable table design for settled trades. | DB Admin | Open |
