# WF-801 Canonical Market Adapter SDK

## Version history

- 1.0.0 (2026-08-23): Initial multi-market contract.

Every adapter resolves market, venue, internal instrument ID, display symbol, base/quote/settlement currency, contract multiplier, tick size and calendar; converts source timestamps to aware UTC; and produces cost-inclusive monetary net return in the declared currency. Core analytics receives the same canonical trade shape regardless of market and never branches on FX/futures/crypto. Market-specific expiry, funding, rolls, sessions and multipliers live in adapters and versioned reference data. FX’s existing `EUR/GBP → EUR_GBP`, GBP monetary return and 24×5 semantics remain unchanged.

