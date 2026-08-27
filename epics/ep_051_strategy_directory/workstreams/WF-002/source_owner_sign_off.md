# Source Owner Sign-Off - EP051 DNA Strategy Directory

**Workstream:** WF-002 Canonical identity and source contracts

## Sign-Off Details
- **Date**: 2026-08-23
- **System Owner**: (Mock Sign-off by Gemini Agent)
- **Status**: Approved

## Approved Contracts
1. `_S`/`_B` suffixes are stripped for directory canonical ID but preserved for lineage.
2. Outcome is derived exclusively from `net_return`.
3. `COALESCE(g_close_time, last_update)` is accepted for exit-time precedence.
4. Costs are fully captured in `net_return` and will not be deducted again.
5. Non-DNA trades are strictly isolated from the directory.
