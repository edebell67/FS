# WF-401 Leakage Test

PASS — WF401 consumes only WF104 observations whose `available_at` is not later than the trade exit/event timestamp. Future observations are rejected by WF104 tests and are absent from regime group input. Definition version 1.0.0 was frozen by WF004 before strategy outcomes were inspected.

