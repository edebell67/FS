# epics/ep_057_sql_to_pgsql/scenario_engine_v2/tests/test_intelligence.py — strategy intelligence: ranking, correlation groups, spread widening / collapsing, no look-ahead.
#
# VERSION HISTORY
# v1.0.0 · 2026-10-17 · Initial version (synthetic curves with known structure).
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from engine import intelligence as intel  # noqa: E402


def model(mid, vals):
    return {"model": mid, "series": [{"time": f"{i // 12:02d}:{(i % 12) * 5:02d}", "net": v} for i, v in enumerate(vals)]}


def wave(n, f=0.3):
    return [10 * math.sin(i * f) + i * 0.5 for i in range(n)]


def curves(n=120):
    base = wave(n)
    a = base
    b = [x + (0 if i < 80 else (i - 80) * 3) for i, x in enumerate(base)]          # tracks A, then pulls away from index 80: the spread widens
    c = [(i * 7919 % 13) * 2.0 - 12 + i * 0.1 for i in range(n)]                   # unrelated
    return [model("A", a), model("B", b), model("C", c)]


def test_top_performers_are_ranked_with_drawdown_and_momentum():
    r = intel.report(curves(), top_n=2)
    assert [t["model"] for t in r["top"]] == ["B", "A"] or r["top"][0]["net"] >= r["top"][1]["net"]
    assert r["top"][0]["rank"] == 1 and r["top"][0]["max_drawdown"] <= 0 and "momentum" in r["top"][0] and len(r["top"]) == 2


def test_correlated_strategies_form_a_group_and_the_unrelated_one_does_not():
    r = intel.report(curves(), as_of_index=79, corr_threshold=0.8)
    groups = [g["members"] for g in r["clusters"]]
    assert ["A", "B"] in groups and all("C" not in g for g in groups)


def test_a_widening_spread_is_flagged_with_its_evidence():
    r = intel.report(curves(), as_of_index=100, window=40, corr_threshold=0.5, z_hi=1.5)
    sig = next(s for s in r["spread_signals"] if s["pair"] == ["A", "B"])
    assert sig["state"] in ("widening", "stretched") and abs(sig["z"]) >= 1.5 and sig["leader"] == "B" and sig["z"] < 0   # B pulls away above A, so spread = A - B is negative
    assert sig["window"] == 40


def test_the_report_uses_no_data_after_the_as_of_point():
    full = curves(120)
    cut = [model(m["model"], [p["net"] for p in m["series"]][:81]) for m in full]
    a = intel.report(full, as_of_index=80)
    b = intel.report(cut)
    for k in ("top", "clusters", "spread_signals", "sample_points", "as_of"):
        assert a[k] == b[k]
    assert a["as_of"] == full[0]["series"][80]["time"]


def test_thin_samples_say_so():
    r = intel.report([model("A", [1, 2, 3, 4]), model("B", [1, 1, 2, 2])])
    assert r["confidence"] == "low" and any("weak" in c for c in r["caveats"]) and any("fewer than three" in c for c in r["caveats"])


def test_max_drawdown_is_the_worst_peak_to_trough_fall():
    top = intel.top_performers({"X": [0, 10, 5, 12, 4, 6]}, {"X": "t"}, 1)[0]
    assert top["max_drawdown"] == -8 and top["net"] == 6 and top["momentum"] == 6 - 0


def test_spread_needs_at_least_eight_points():
    assert intel.spread_signal("A", "B", [1.0] * 7, [0.0, 1, 0, 1, 0, 1, 0]) is None
    assert intel.spread_signal("A", "B", [float(i % 3) for i in range(8)], [0.0] * 8) is not None


def _spread(values):
    return intel.spread_signal("A", "B", values, [0.0] * len(values), window=len(values), z_hi=1.5)


def test_spread_states_widening_collapsing_stretched_normal():
    flat = [0.0, 0.2, -0.1, 0.1, 0.0, -0.2, 0.1, 0.0, 0.1, -0.1, 0.0, 0.1]
    widening = flat + [0.8, 1.6, 3.0, 5.0]               # |z| climbing past the threshold
    collapsing = flat + [5.0, 5.0, 5.0, 1.5, 0.3, 0.0]   # was far out, is coming back
    stretched = flat + [5.0, 5.0, 5.0, 5.0, 5.0]         # far out and not moving
    assert _spread(widening)["state"] == "widening"
    assert _spread(collapsing)["state"] == "collapsing"
    assert _spread(stretched)["state"] == "stretched"
    assert _spread(flat)["state"] == "normal"
