import json
import time
import requests
from datetime import datetime

# Test URLs
PAGES = [
    {"name": "Strongest Models", "url": "https://edebell67.github.io/epics/models/"},
    {"name": "Early Momentum", "url": "https://edebell67.github.io/epics/momentum/"},
    {"name": "Verifiable Data", "url": "https://edebell67.github.io/epics/verify/"},
    {"name": "Ranked Feed", "url": "https://edebell67.github.io/epics/ranked/"}
]

BACKEND_STATS_URL = "https://ep-017.onrender.com/api/stats"

def get_current_stats():
    try:
        resp = requests.get(BACKEND_STATS_URL, timeout=15)
        if resp.ok:
            return resp.json()
    except Exception as e:
        print(f"Error fetching stats: {e}")
    return None

print(f"--- EP017 Lead Capture Verification [{datetime.now()}] ---")

# 1. Get baseline stats
initial_stats = get_current_stats()
print(f"Initial Stats: {initial_stats}")

print("\nTriggering a lead capture via direct POST to verify backend functional health...")

test_email = f"test_{int(time.time())}@example.com"
payload = {
    "email": test_email,
    "page_id": "verification_script", # Fixed field name
    "pain_point_key": "gemini_cli_test"
}

try:
    resp = requests.post("https://ep-017.onrender.com/api/capture_lead", json=payload, timeout=15)
    print(f"Direct POST Result: {resp.status_code} {resp.text}")
    
    if resp.ok:
        print("Waiting for stats sync (Render disk persistence check)...")
        time.sleep(5) 
        new_stats = get_current_stats()
        print(f"New Stats: {new_stats}")
        
        if new_stats and "verification_script" in new_stats:
            print("\n✅ SUCCESS: Lead capture backend is functional and recording data.")
        else:
            print("\n⚠️ WARNING: New lead not found in stats. Backend might be using memory-only store or sync delay.")
except Exception as e:
    print(f"Capture Test Failed: {e}")

print("\n--- End of Verification ---")
