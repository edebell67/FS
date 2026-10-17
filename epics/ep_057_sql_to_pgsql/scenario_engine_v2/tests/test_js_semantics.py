# epics/ep_057_sql_to_pgsql/scenario_engine_v2/tests/test_js_semantics.py — small JavaScript behaviours the port must reproduce, checked directly against Node.
#
# VERSION HISTORY
# v1.0.0 · 2026-10-17 · Number.toFixed (exact ties round up) and Math.round, over a grid that includes the .5 ties the random differential data almost never hits.
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from engine import core_ported as core  # noqa: E402
from engine import replay_models as rm  # noqa: E402

pytestmark = pytest.mark.skipif(not shutil.which("node"), reason="needs node")


def _node(script: str):
    r = subprocess.run(["node", "-e", script], capture_output=True, text=True, encoding="utf-8")
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)


VALUES = [0, 0.5, 1.5, 2.5, 504.5, 505.5, -504.5, -0.5, -1.5, 0.125, 0.375, 1.005, 2.675, 1.45, 8.345, 1e-7, 123456.789, 0.049, -0.049, 10, -10, 99.995, 1e21, -1e21, 4.35, 0.285]


@pytest.mark.parametrize("digits", [0, 1, 2])
def test_to_fixed_matches_javascript(digits):
    want = _node(f"console.log(JSON.stringify({json.dumps(VALUES)}.map(v => v.toFixed({digits}))))")
    got = [core.js_to_fixed(v, digits) for v in VALUES]
    assert got == want


def test_to_fixed_special_values():
    assert core.js_to_fixed(float("nan")) == "NaN" and core.js_to_fixed(float("inf")) == "Infinity" and core.js_to_fixed(float("-inf")) == "-Infinity"


def test_math_round_matches_javascript():
    values = [0.5, 1.5, 2.5, -0.5, -1.5, -2.5, 2.4999999, 100.5, -100.5]
    want = _node(f"console.log(JSON.stringify({json.dumps(values)}.map(v => Math.round(v))))")
    assert [rm.js_round(v) for v in values] == want
