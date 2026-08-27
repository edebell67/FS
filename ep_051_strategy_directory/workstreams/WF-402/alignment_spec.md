# WF-402 Alignment Specification

V1 frequency is UTC calendar day. Closed trades are first aggregated to strategy/day; asynchronous trade rows are never directly correlated. For a confirmed eligible market day with complete source coverage, no closed trade becomes zero P&L. A missing/incomplete source day remains null and is excluded, never silently zero-filled. Pair overlap requires at least 30 jointly valid daily observations and reports overlap ratio, first/last aligned dates and methodology version.

