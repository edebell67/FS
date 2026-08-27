# VERSION HISTORY
# v1.1.0 · 2026-08-24 · Ensures discovery caches one batch curve load.
# v1.0.0 · 2026-08-24 · Ensures discovery builds every profile from one batch curve load.
from fastapi.testclient import TestClient
from app.config import Settings
from app.main import create_app


def test_discovery_never_triggers_batch_series_load(monkeypatch):
    import app.main as module
    calls={"batch":0}
    monkeypatch.setattr(module,"local_strategies",lambda settings:[{"strategy_id":"DNA_1","market":"FX","product_name":"EURUSD","total_trades":2,"wins":2,"losses":0,"breakevens":0,"total_net_return":3,"win_rate":1,"profit_factor":None,"max_drawdown_money":0,"quality_state":"COLLECTING"}])
    def batch(settings,*args):
        calls["batch"]+=1
        return {"DNA_1":[{"closed_at":"2024-01-01T00:00:00+00:00","net_return":1},{"closed_at":"2025-01-02T00:00:00+00:00","net_return":2}]}
    monkeypatch.setattr(module,"local_equity_curves",batch)
    client=TestClient(create_app(settings=Settings(data_backend="sqlserver",db_server="x",db_user="x",db_pass="x",local_intelligence_cache_path="runtime/__missing_intelligence_cache_for_test__.json",allow_synchronous_local_fallback=True)))
    response=client.post("/api/intelligence/query/search",json={"plan":{"asset_class":"FX"}})
    second=client.post("/api/intelligence/query/search",json={"plan":{"asset_class":"FX"}})
    assert response.status_code==200 and second.status_code==200 and response.json()["total"]==1 and calls["batch"]==0
