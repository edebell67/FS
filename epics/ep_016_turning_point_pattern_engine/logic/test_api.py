import json
import time
from urllib.request import urlopen

HTTP_SOURCE_URL = "http://127.0.0.1:8002/api/vw_000_fx_quotes"

def fetch_quotes():
    print(f"Connecting to {HTTP_SOURCE_URL}...")
    try:
        with urlopen(HTTP_SOURCE_URL, timeout=5) as response:
            payload = json.load(response)
        print("Successfully fetched quotes.")
        return payload.get("data", [])
    except Exception as e:
        print(f"Error fetching quotes: {e}")
        return []

quotes = fetch_quotes()
if quotes:
    print(f"Received {len(quotes)} symbols.")
    print(json.dumps(quotes[0], indent=2))
else:
    print("No quotes received.")
