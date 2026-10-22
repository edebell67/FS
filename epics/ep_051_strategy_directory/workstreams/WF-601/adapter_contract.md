# WF-601 Broker Adapter Contract

## Version history

- 1.0.0 (2026-08-23): Initial deferred, offline-only adapter contract.

This node defines an integration seam; it does not integrate a live broker. The only implementation is deterministic and in-memory, has no network transport, accepts no credential fields, and cannot reach or mutate an account.

Canonical strategy IDs remain separate from broker instrument IDs. A versioned mapping resolves internal instrument IDs to explicitly supported sandbox symbols. The adapter exposes capabilities before any intent: MARKET orders and ACK/FILL/REJECT/CANCEL synthetic events are supported; live accounts, credentials, withdrawals, options and network transport are unsupported.

An order intent contains an idempotency ID, canonical strategy ID, internal instrument ID, side, positive quantity and order type. Events retain the intent ID. Unsupported instruments and invalid orders reject safely. Production implementations must preserve this contract, retrieve secrets server-side from an approved vault, redact logs, require separate deployment approval, and pass the same contract suite before activation.

