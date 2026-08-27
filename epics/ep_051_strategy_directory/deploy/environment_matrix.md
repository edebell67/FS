# EP051 Environment Matrix and Secret Boundaries

## Version history

- 1.0.0 (2026-08-23): Initial environment contract.

| Setting | Local | Beta | Production | Secret? | Browser allowed? |
|---|---|---|---|---|---|
| Environment/ports/log level | explicit template | deployment config | deployment config | No | Only public base URL |
| DB name/user | template | platform config | platform config | Internal | No |
| DB password | local secret store | vault reference | rotated vault reference | Yes | Never |
| Snapshot/version/TTLs | template | release config | release config | No | Safe evidence metadata only |
| Broker profile | disabled | disabled | disabled until separate approval | No | Status only |
| Future broker credential | absent | absent | server-side vault only | Yes | Never |

`.env.example` contains placeholders, not usable secrets. Actual `.env`, vault exports, credential files and database dumps are excluded from source control and artifact exports. Services receive only the variables they require. Logs redact values by key and classification; clients receive allowlisted public fields. Production rejects default/placeholder secrets, prohibits debug, binds databases/caches privately and separates read/write/migration identities.

