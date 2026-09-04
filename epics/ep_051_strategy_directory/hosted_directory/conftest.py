"""Test bootstrap for the EP051 DNA Strategy Directory package.

Version history:
- 1.0.0 (2026-09-04): Initial version. The intelligence implementation
  (app/intelligence/*, app/arena_provider.py) moved to
  epics/ep_049_strategy_intelligence/hosted_directory/ per Ed's EP049
  ownership decision, but several tests that remain here (and app/main.py
  itself, the shared FastAPI host) still import app.intelligence.* /
  app.arena_provider. Both directories' app/ packages are Python
  namespace packages (no __init__.py) that merge into one `app` import
  namespace when both are on sys.path, which is what this file sets up
  for pytest collection.
"""
from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_EP049_HOSTED_DIRECTORY = _HERE.parent.parent / "ep_049_strategy_intelligence" / "hosted_directory"

for _path in (str(_HERE), str(_EP049_HOSTED_DIRECTORY)):
    if _path not in sys.path:
        sys.path.insert(0, _path)
