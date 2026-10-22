from copy import deepcopy
from datetime import datetime,timedelta,timezone

import pytest

from app.intelligence.cache import SCHEMA_VERSION,cache_hash,validate_local_cache,validate_local_cache_freshness
from app.intelligence.profile import build_profile


def payload():
    points=[{"trade_number":1,"opened_at":"2026-08-24T08:00:00Z","closed_at":"2026-08-24T09:00:00Z","net_return":2,"equity":2,"drawdown":0}]
    profile=build_profile({"strategy_id":"DNA_1","market":"FX","product_name":"EURUSD"},points).model_dump(mode="json")
    result={"schema_version":SCHEMA_VERSION,"generated_at":datetime.now(timezone.utc).isoformat(),"catalog_size":1,"profile_depth":"full","profiles":[profile],"curves":{"DNA_1":points}}
    result["sha256"]=cache_hash(result);return result


def test_cache_digest_and_age_are_rechecked():
    item=payload();assert validate_local_cache(item,3600)
    tampered=deepcopy(item);tampered["curves"]["DNA_1"][0]["net_return"]=99
    with pytest.raises(ValueError,match="digest"):validate_local_cache(tampered,3600)
    stale=payload();stale["generated_at"]=(datetime.now(timezone.utc)-timedelta(hours=2)).isoformat();stale["sha256"]=cache_hash(stale)
    with pytest.raises(ValueError,match="stale"):validate_local_cache(stale,3600)


def test_unchanged_validated_cache_still_expires_on_each_access():
    item=payload();generated=datetime.fromisoformat(item["generated_at"])
    assert validate_local_cache_freshness(item,60,now=generated)
    with pytest.raises(ValueError,match="stale"):validate_local_cache_freshness(item,60,now=generated+timedelta(seconds=61))
