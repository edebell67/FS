# epics/ep_057_sql_to_pgsql/scenario_engine_v2/tests/test_criteria_hash.py — the page sends the scenario data once per content hash.
from engine import command
from engine.page_state import PageState


def _req(**extra):
    return {"method": "pause_replay", "args": [], "state": PageState().snapshot(), **extra}


def test_hash_without_data_asks_for_it_then_uses_cache(monkeypatch):
    command._CRITERIA_CACHE.clear()
    assert command.run(_req(criteriaHash="h1")) == {"needCriteria": True}


def test_cache_is_bounded():
    command._CRITERIA_CACHE.clear()
    for i in range(10):
        command._CRITERIA_CACHE[f"k{i}"] = {}
        while len(command._CRITERIA_CACHE) > 4:
            command._CRITERIA_CACHE.pop(next(iter(command._CRITERIA_CACHE)))
    assert len(command._CRITERIA_CACHE) == 4
