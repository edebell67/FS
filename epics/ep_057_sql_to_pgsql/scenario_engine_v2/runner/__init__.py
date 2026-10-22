# epics/ep_057_sql_to_pgsql/scenario_engine_v2/runner/__init__.py — virtual race runner: many isolated Engine instances in parallel.
#
# VERSION HISTORY
# v1.0.0 · 2026-10-17 · Initial version.
import os
import sys

# the runner imports the engine package that sits next to it
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from .manager import DEFAULT_MAX_CONCURRENT, RaceManager  # noqa: E402,F401
from .race import Race, RaceConfig  # noqa: E402,F401
