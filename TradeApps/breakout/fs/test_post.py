import requests
import json

payload = {
    "name": "test_single_strat_multi_metric",
    "mode": "live",
    "strategies": [
        "breakout_test | gbp_usd | buy_net",
        "breakout_test | gbp_usd | sell_net"
    ]
}

try:
    resp = requests.post('http://127.0.0.1:5000/api/trade_buckets', json=payload)
    print(resp.status_code)
    print(resp.json())
except Exception as e:
    print(e)
