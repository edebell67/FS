import json
import os
from datetime import datetime
from pathlib import Path
from paths import BREAKOUT_JSON_ROOT

BASE_DIR = BREAKOUT_JSON_ROOT / "live"
DATE_STR = datetime.now().strftime("%Y-%m-%d")

def get_top_performer(asset_class):
    path = BASE_DIR / asset_class / DATE_STR / "_frequency.json"
    if not path.exists():
        return None
    
    try:
        with open(path, 'r') as f:
            data = json.load(f)
            leaders = data.get("leaders", [])
            if not leaders:
                return None
            return leaders[0]
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return None

def get_dna_top_performer():
    path = BASE_DIR / "forex" / DATE_STR / "_dna_frequency.json"
    if not path.exists():
        return None

    try:
        with open(path, 'r') as f:
            data = json.load(f)
            leaders = data.get("leaders", [])
            if not leaders:
                return None
            return leaders[0]
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return None

def format_summary():
    results = []

    # Check regular assets
    for ac in ["forex", "crypto", "metals", "indices", "energy"]:
        top = get_top_performer(ac)
        if top and top.get("final_net", 0) > 0:
            results.append({
                "class": ac.capitalize(),
                "product": top["product"],
                "net": top["final_net"]
            })

    # Check DNA
    dna_top = get_dna_top_performer()
    if dna_top and dna_top.get("final_net", 0) > 0:
        results.append({
            "class": "DNA",
            "product": dna_top["product"],
            "net": dna_top["final_net"]
        })

    if not results:
        return "Market Battle Update: Quiet session so far. Top strategies are positioning for the next move. \n\nLive tracking: https://piphunter.io #PipHunter #Trading"

    # Sort by net return
    results.sort(key=lambda x: x["net"], reverse=True)

    tweet = "📊 MARKET BATTLE SUMMARY\n"
    tweet += f"Date: {DATE_STR}\n\n"

    for res in results[:4]:
        emoji = "🟢" if res["net"] > 0 else "🔴"
        tweet += f"{emoji} {res['class']} Leader: {res['product']} (+{res['net']:.0f})\n"

    tweet += "\n👑 Top performers emerging.\n"
    tweet += "Public dashboard coming soon.\n\n"
    tweet += "Live stats: https://piphunter.io\n"
    tweet += "#PipHunter #Trading #Forex"

    return tweet

if __name__ == "__main__":
    tweet_text = format_summary()
    print("--- TWEET CONTENT ---")
    print(tweet_text)
    print("--- END CONTENT ---")

    # Save to a temp file for the next step
    with open("temp_tweet.txt", "w", encoding="utf-8") as f:
        f.write(tweet_text)
